import json

with open('C:\\Users\\shikh\\Desktop\\ssc-prep-platform\\backend\\data\\imports\\general-banking-awareness\\verified_batch.json') as f:
    data = json.load(f)

print('Total questions:', len(data['questions']))
print('Chapter counts:', data['chapter_counts'])
print()

# Check all question structures
for i, q in enumerate(data['questions']):
    cid = q['chapter_id'][:8]
    opts = q.get('options')
    ans = q.get('correct_answer')
    src = q.get('source_metadata')
    print(f'Q{i}: chapter_id={cid}... options_type={type(opts).__name__} len={len(opts) if opts else 0} answer={ans} source_meta={src}')