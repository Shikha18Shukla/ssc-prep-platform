import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

print("All subjects in the database:")
cur.execute("SELECT id, name, slug, subject_id, exam_id FROM subjects ORDER BY id")
subjects = cur.fetchall()
for sid, sname, sslug, subj_id, exam_id in subjects:
    print(f"  ID: {str(sid)[:20]}... | Name: {sname[:50]} | Slug: {sslug[:30]} | Subject_id: {str(subj_id)[:20]}... | Exam_id: {str(exam_id)[:20]}...")

conn.close()