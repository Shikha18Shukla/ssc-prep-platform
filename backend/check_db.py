import subprocess
result = subprocess.run(
    ['psql', '-h', '127.0.0.1', '-U', 'postgres', '-d', 'ssc_prep', '-c', '\dt'],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)