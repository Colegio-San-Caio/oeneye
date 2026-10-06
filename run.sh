#!/data/data/com.termux/files/usr/bin/bash
cd ~/oeneye
nohup python app.py > flask.log 2>&1 &
nohup cloudflared tunnel --url http://127.0.0.1:5000 > tunnel.log 2>&1 &
echo "both started, cat flask.log / tunnel.log to check"
