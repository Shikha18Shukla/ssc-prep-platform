import json
from collections import Counter
import pytest
from sqlalchemy import func,select
from app.models import Chapter,Difficulty,Exam,Question,QuestionOption,Subject,Subcategory
from app.services.question_import_service import import_questions
from scripts.import_race_verified_batch import BATCH,load_batch,plan_missing

@pytest.fixture
def race_catalog(db_session):
 exam=Exam(name="SSC",slug="ssc",is_active=True); db_session.add(exam); db_session.flush()
 subject=Subject(exam_id=exam.id,name="Maths",slug="maths",is_active=True); db_session.add(subject); db_session.flush()
 category=Subcategory(subject_id=subject.id,name="Arithmetic Maths",slug="arithmetic-maths",is_active=True); db_session.add(category); db_session.flush()
 chapter=Chapter(subject_id=subject.id,subcategory_id=category.id,name="Race",slug="race",is_active=True); db_session.add(chapter); db_session.commit(); return chapter

def test_planner_targets_and_preserves_existing_rows():
 rows=load_batch(); assert len(rows)==90
 assert Counter(r["difficulty"] for r in rows)=={"EASY":30,"MEDIUM":30,"HARD":30}
 assert plan_missing(rows,[])==rows

def test_dry_run_import_and_replay_are_idempotent(db_session,race_catalog):
 data=BATCH.read_bytes(); preview=import_questions(db_session,data,"application/json",BATCH.name,True)
 assert not preview.aborted and not preview.errors and preview.would_import==90 and preview.duplicates==0
 assert db_session.scalar(select(func.count(Question.id)))==0
 result=import_questions(db_session,data,"application/json",BATCH.name,False)
 assert result.imported==90 and result.duplicates==0 and not result.errors
 rows=db_session.scalars(select(Question).where(Question.chapter_id==race_catalog.id)).all()
 assert Counter(q.difficulty.value for q in rows)=={"EASY":30,"MEDIUM":30,"HARD":30}
 assert all(q.is_active and not q.is_pyq for q in rows) and plan_missing(load_batch(),rows)==[]
 replay=import_questions(db_session,data,"application/json",BATCH.name,False)
 assert replay.imported==0 and replay.duplicates==90

def test_planner_preserves_matching_existing_question(db_session,race_catalog):
 row=load_batch()[0]; options=[QuestionOption(option_key=k,option_text=row["options"][k],is_correct=k==row["correct_option"],display_order=i) for i,k in enumerate("ABCD",1)]
 q=Question(chapter_id=race_catalog.id,question_text=row["question_text"],explanation=row["explanation"],difficulty=Difficulty(row["difficulty"]),is_pyq=False,is_active=True,source=row["source"],options=options)
 db_session.add(q); db_session.commit()
 selected=plan_missing(load_batch(),[q]); assert len(selected)==89 and row["question_text"] not in {r["question_text"] for r in selected}
