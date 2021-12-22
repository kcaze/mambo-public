from bottle import get, post, request, run, static_file
import subprocess

@get('/<path:re:.*>')
def server_static(path):
  print(path)
  return static_file(path, root='pzprv3/dist')

@post('/solve')
def solve():
  encodedURL = request.body.getvalue().decode()
  process = subprocess.run(
    ["python3", "claspy/solvers/main.py", encodedURL],
    stdout=subprocess.PIPE,
    encoding="utf-8",
    env={
      "PYTHONPATH": "./claspy",
    })
  return process.stdout

run(host='localhost', port=8080, debug=True)
