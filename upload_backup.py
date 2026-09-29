import base64
import json
import urllib.request

# Configuration
token = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
repo = "clevjhon/oeneye"
branch = "packs"
file_path = "oeneye_asset_omq.tar.gz"

with open(file_path, "rb") as f:
    content_encoded = base64.b64encode(f.read()).decode("utf-8")

url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Check if file already exists to get its sha (required for updates)
req = urllib.request.Request(url, headers=headers)
sha = None
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        sha = data.get("sha")
except Exception:
    pass

payload = {
    "message": "Manual upload: OMQ.FNT asset backup bundle",
    "content": content_encoded,
    "branch": branch
}
if sha:
    payload["sha"] = sha

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers=headers, method="PUT")

try:
    with urllib.request.urlopen(req) as response:
        print("[SUCCESS] Backup uploaded successfully to GitHub!")
except urllib.error.HTTPError as e:
    print(f"[ERROR] Failed to upload: {e.code} {e.reason}")
    print(e.read().decode())
