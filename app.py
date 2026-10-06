import os, json, subprocess
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
REPO_DIR = os.path.expanduser("~/oeneye")
LOG_FILE = f"{REPO_DIR}/termuxdb.log"
PID_IMG = f"{REPO_DIR}/PID.ximg"

# AUTO PORT: set PORT=8000 or it defaults to 5000
PORT = int(os.environ.get("PORT", "5000"))

def log_db(e,d={}):
    r={"ts":datetime.now().isoformat(),"event":e,**d}
    open(LOG_FILE,"a").write(json.dumps(r)+"\n")
    open(PID_IMG,"a").write(f"{r['ts']} [{e}] {d}\n")
    print(r)

@app.route("/api/deploy",methods=["POST"])
def deploy():
    j=request.get_json(silent=True) or {}
    b=j.get("ref","refs/heads/main").split("/")[-1]
    log_db("deploy_start",{"branch":b,"port":PORT})
    try:
        env=os.environ.copy()
        env["TMPDIR"]=os.path.expanduser("~/tmp")
        os.makedirs(env["TMPDIR"],exist_ok=True)
        subprocess.run(["git","pull","origin",b],cwd=REPO_DIR,check=True,env=env)
        log_db("git_pull_ok",{"branch":b})
        return jsonify(message=f"Deployed {b} on {PORT}",status="success")
    except Exception as ex:
        log_db("deploy_failed",{"error":str(ex)})
        return jsonify(error=str(ex)),500

@app.route("/")
def health():
    return f"OQM D16S alive on {PORT}"

if __name__=="__main__":
    os.makedirs(os.path.expanduser("~/tmp"),exist_ok=True)
    print(f"Starting on http://127.0.0.1:{PORT}")
    app.run(host="0.0.0.0",port=PORT)
