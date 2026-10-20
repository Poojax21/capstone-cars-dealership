import os, time, subprocess

BASE = r"C:\Users\Hi\Desktop\COUSERA PROJECT\capstone-cars-dealership"
SERVER = os.path.join(BASE, "server")
OUT = os.path.join(BASE, "answers")
PY = r"C:\Users\Hi\AppData\Local\Programs\Python\Python314\python.exe"
CURL = r"C:\Windows\System32\curl.exe"
os.makedirs(OUT, exist_ok=True)

srv = subprocess.Popen(
    [PY, "manage.py", "runserver", "127.0.0.1:8000", "--noreload"],
    cwd=SERVER, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
)
time.sleep(5)

def run(args):
    p = subprocess.run(args, cwd=BASE, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()

def write(name, command, output):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(f"$ {command}\n\n{output}\n")
    print(f"--- {name} ---\n{output[:300]}\n")

cookies = os.path.join(BASE, "answers", "cookies.txt")
if os.path.exists(cookies):
    os.remove(cookies)

login_args = [CURL, "-s", "-X", "POST", "-d", "userName=testuser&password=testpass123",
              "-c", "answers/cookies.txt", "http://localhost:8000/djangoapp/login"]
login_cmd = 'curl -X POST -d "userName=testuser&password=testpass123" -c cookies.txt http://localhost:8000/djangoapp/login'

logout_args = [CURL, "-s", "-X", "POST", "-b", "answers/cookies.txt",
               "http://localhost:8000/djangoapp/logout"]
logout_cmd = 'curl -X POST -b cookies.txt http://localhost:8000/djangoapp/logout'

try:
    write("loginuser", login_cmd, run(login_args))
    write("logoutuser", logout_cmd, run(logout_args))

    simple = {
        "getdealerreviews": "http://localhost:8000/djangoapp/reviews/dealer/1",
        "getalldealers": "http://localhost:8000/djangoapp/get_dealers/",
        "getdealerbyid": "http://localhost:8000/djangoapp/dealer/1",
        "getdealersbyState": "http://localhost:8000/djangoapp/get_dealers/Kansas",
        "getallcarmakes": "http://localhost:8000/djangoapp/get_cars/",
        "analyzereview": "http://localhost:8000/djangoapp/analyze/Fantastic%20services",
    }
    for name, url in simple.items():
        write(name, f"curl {url}", run([CURL, "-s", url]))
finally:
    srv.terminate()
    try:
        log = srv.communicate(timeout=5)[0]
    except Exception:
        log = ""
    with open(os.path.join(OUT, "django_server"), "w", encoding="utf-8") as f:
        f.write(log or "")

print("DONE")