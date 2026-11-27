"""Import English Language questions for Banking Clerk and Banking PO.

Loads `data/english_grammar_questions.json`, validates every chapter before
touching the database, and inserts each question into the matching chapter of
both exams. The import is idempotent: question text is normalised and used to
derive a stable UUID, and existing active texts are skipped.

The dataset currently covers 15 chapters (40 questions each). Add more chapter
slugs to the JSON and the importer handles them without code changes.
"""

import argparse
import json
import os
import unicodedata
import uuid
from datetime import datetime

import psycopg2

DB_URL = 'postgresql://postgres@127.0.0.1:5432/ssc_prep'
CLERK_SID = 'a6ee9965-05c6-4d48-8ce6-855bc5d8d462'
PO_SID = '9de51dcf-a850-4713-afce-edffb7b4ece9'

EXPECTED_PER_CHAPTER = 40
VALID_DIFFICULTIES = {'EASY', 'MEDIUM', 'HARD'}
VALID_KEYS = set('ABCDE')

# Fixed namespace so the same question always receives the same UUID in a chapter.
QUESTION_NAMESPACE = uuid.UUID('6f1c2a54-8d3b-5e7a-9c41-2b8f0d6e7a13')


def normalize_text(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def stable_question_id(chapter_id, norm_text):
    return str(uuid.uuid5(QUESTION_NAMESPACE, f"{chapter_id}:{norm_text}"))


def validate_dataset(all_questions):
    """Validate the whole dataset before touching the database."""
    if not isinstance(all_questions, dict) or not all_questions:
        raise ValueError('Dataset must be a non-empty JSON object keyed by chapter slug')

    seen_by_chapter = {}
    for slug, questions in all_questions.items():
        if len(questions) != EXPECTED_PER_CHAPTER:
            raise ValueError(f"{slug}: expected {EXPECTED_PER_CHAPTER} questions, found {len(questions)}")

        seen = set()
        for idx, q_data in enumerate(questions, start=1):
            if not isinstance(q_data, (list, tuple)) or len(q_data) != 5:
                raise ValueError(f"{slug} #{idx}: expected [text, options, key, difficulty, explanation]")

            q_text, opts, correct, diff, expl = q_data
            if not isinstance(q_text, str) or not q_text.strip():
                raise ValueError(f"{slug} #{idx}: empty question text")
            if not isinstance(opts, (list, tuple)) or len(opts) != 5:
                raise ValueError(f"{slug} #{idx}: expected exactly 5 options")
            if len(set(opts)) != 5:
                raise ValueError(f"{slug} #{idx}: duplicate options")
            for opt_idx, opt in enumerate(opts):
                expected_prefix = chr(65 + opt_idx) + ')'
                if not isinstance(opt, str) or not opt.startswith(expected_prefix):
                    raise ValueError(f"{slug} #{idx}: option {opt_idx + 1} must start with {expected_prefix}")
            if correct not in VALID_KEYS:
                raise ValueError(f"{slug} #{idx}: invalid answer key {correct!r}")
            if diff not in VALID_DIFFICULTIES:
                raise ValueError(f"{slug} #{idx}: invalid difficulty {diff!r}")
            if not isinstance(expl, str) or not expl.strip():
                raise ValueError(f"{slug} #{idx}: empty explanation")

            norm = normalize_text(q_text)
            if norm in seen:
                raise ValueError(f"{slug} #{idx}: duplicate question text: {q_text}")
            seen.add(norm)

        seen_by_chapter[slug] = seen

    # Reject the same question appearing in two different chapters.
    owners = {}
    for slug, texts in seen_by_chapter.items():
        for norm in texts:
            if norm in owners:
                raise ValueError(f"duplicate question in {owners[norm]!r} and {slug!r}: {norm[:80]}")
            owners[norm] = slug

    return seen_by_chapter


def get_chapter_id(cur, sid, slug):
    cur.execute("SELECT id FROM chapters WHERE subject_id = %s AND slug = %s", (sid, slug))
    row = cur.fetchone()
    if not row:
        raise LookupError(f"Chapter slug {slug!r} not found for subject {sid}")
    return row[0]


def get_existing_texts(cur, chapter_id):
    cur.execute(
        "SELECT question_text FROM questions WHERE chapter_id = %s::uuid AND is_active = true",
        (chapter_id,),
    )
    return set(normalize_text(r[0]) for r in cur.fetchall())


def insert_question(cur, ch_id, q_data):
    q_text, opts, correct, diff, expl = q_data
    norm = normalize_text(q_text)
    qid = stable_question_id(ch_id, norm)
    now = datetime.now()
    cur.execute("""
        INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url)
        VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (qid, ch_id, q_text, expl, diff, False, None, None, 'original-practice', True, now, now, None))

    for idx, opt_text in enumerate(opts):
        opt_key = chr(65 + idx)
        is_correct = (opt_key == correct)
        cur.execute("""
            INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), qid, opt_key, opt_text, idx + 1, is_correct))

    return qid


def main():
    parser = argparse.ArgumentParser(description='Import English grammar questions for Banking Clerk and Banking PO.')
    parser.add_argument('--dry-run', action='store_true', help='Validate and report without writing to the database')
    args = parser.parse_args()

    json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'english_grammar_questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)

    validate_dataset(all_questions)
    print(f"Dataset validated: {len(all_questions)} chapters, "
          f"{sum(len(v) for v in all_questions.values())} questions")

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    total_inserted = 0
    try:
        for slug, questions in all_questions.items():
            clerk_ch_id = get_chapter_id(cur, CLERK_SID, slug)
            po_ch_id = get_chapter_id(cur, PO_SID, slug)

            clerk_existing = get_existing_texts(cur, clerk_ch_id)
            po_existing = get_existing_texts(cur, po_ch_id)

            inserted_clerk = 0
            inserted_po = 0

            for q_data in questions:
                norm = normalize_text(q_data[0])

                if norm not in clerk_existing:
                    insert_question(cur, clerk_ch_id, q_data)
                    clerk_existing.add(norm)
                    inserted_clerk += 1

                if norm not in po_existing:
                    insert_question(cur, po_ch_id, q_data)
                    po_existing.add(norm)
                    inserted_po += 1

            total_inserted += inserted_clerk + inserted_po
            print(f"{slug}: inserted {inserted_clerk} to Clerk, {inserted_po} to PO "
                  f"(now {len(clerk_existing)} / {len(po_existing)} active)")

        if args.dry_run:
            conn.rollback()
            print(f"\nDry run: rolled back, would have inserted {total_inserted}")
        else:
            conn.commit()
            print(f"\nTotal inserted: {total_inserted}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()
