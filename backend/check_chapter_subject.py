import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Get all banking chapters with their subject_id
cur.execute("SELECT id, name, subject_id, subcategory_id FROM chapters WHERE subject_id IS NOT NULL ORDER BY name")
chapters = cur.fetchall()
for cid, cname, subj_id, subcat_id in chapters:
    cname_short = cname[:50] if cname else "None"
    subj_short = str(subj_id)[:20] if subj_id else "None"
    print(f"  {cname_short}: chapter_id={str(cid)[:20]}..., subject_id={subj_short}, subcategory_id={str(subcat_id)[:20] if subcat_id else 'None'}")

conn.close()