import psycopg2
import uuid
import psycopg2.extras

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
psycopg2.extras.register_uuid(conn)

# Test inserting a UUID
cur = conn.cursor()
test_uuid = uuid.UUID('222c866b-71a3-4277-95e5-1af657ed49a9')
print(f'UUID object: {test_uuid}')
print(f'UUID type: {type(test_uuid)}')

# Try inserting
cur.execute('SELECT %s::uuid', (test_uuid,))
result = cur.fetchone()
print(f'Result: {result}')

conn.close()
print('UUID test successful')