import json, uuid
from sqlalchemy import select
import sys
sys.path.insert(0,'backend')
from app.database.session import SessionLocal
from app.models import Question, QuestionOption
from app.models.question import Difficulty

PO_CHAPTER_ID = uuid.UUID('4c6d53e5-46b3-4f0a-a71a-e5696e4f70ed')
DEFAULT_SECTION = 'banking_po_current_affairs_test_1'

db = SessionLocal()
data = json.load(open('data/banking_po_current_affairs_questions.json', encoding='utf-8-sig'))
added = 0
for item in data:
    section = item.get('section', DEFAULT_SECTION)
    exists = db.execute(select(Question).where(Question.chapter_id==PO_CHAPTER_ID, Question.question_text==item['question_text'])).scalar_one_or_none()
    if exists:
        continue
    q = Question(chapter_id=PO_CHAPTER_ID, question_text=item['question_text'], difficulty=Difficulty.MEDIUM, is_pyq=False, is_active=True, section=section)
    db.add(q)
    db.flush()
    for key, txt in item['options'].items():
        db.add(QuestionOption(question_id=q.id, option_key=key, option_text=txt, display_order=ord(key)-64, is_correct=(key==item['correct_option'])))
    added += 1
db.commit()
print('added this run:', added)
for sec in ['banking_po_current_affairs_test_1','banking_po_current_affairs_test_2','banking_po_current_affairs_test_3']:
    count = len(db.execute(select(Question).where(Question.chapter_id==PO_CHAPTER_ID, Question.section==sec)).scalars().all())
    print(sec, count)
db.close()
