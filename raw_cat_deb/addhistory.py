import subprocess, re, html, sys, shutil, os

N = sys.argv[1] if len(sys.argv) > 1 else '200'
S, E = '<!-- COMMIT-HISTORY-START -->', '<!-- COMMIT-HISTORY-END -->'

def git(*a):
    return subprocess.run(['git'] + list(a), capture_output=True, text=True).stdout.strip()

log = git('log', '-n', N, '--date=short', '--pretty=format:%h%x1f%H%x1f%ad%x1f%an%x1f%s')
if not log:
    sys.exit("No commits found. Run this inside your repo folder.")

base = git('remote', 'get-url', 'origin')
base = re.sub(r'\.git$', '', base)
base = re.sub(r'^git@github\.com:', 'https://github.com/', base)
base = re.sub(r'^https://[^@/]+@', 'https://', base)
if 'github.com' not in base:
    base = ''

items = ''
for line in log.split('\n'):
    short, full, date, author, subj = line.split('\x1f')
    h = html.escape(short)
    if base:
        h = '<a href="%s/commit/%s">%s</a>' % (base, full, h)
    items += '<li><code>%s</code> <span class="d">%s</span> %s <span class="a">&mdash; %s</span></li>\n' % (
        h, date, html.escape(subj), html.escape(author))

block = (S + '\n<section id="commit-history">\n<style>\n'
    '#commit-history{margin:24px 0;font-family:monospace}\n'
    '#commit-history ul{list-style:none;padding:0;margin:0}\n'
    '#commit-history li{padding:6px 0;border-bottom:1px solid #2a3644}\n'
    '#commit-history code{color:#7fd1ae}\n'
    '#commit-history .d{opacity:.6}\n'
    '#commit-history .a{opacity:.6;font-size:.85em}\n'
    '</style>\n<h2>Commit History</h2>\n<ul>\n' + items + '</ul>\n</section>\n' + E)

if not os.path.isfile('index.html'):
    sys.exit("index.html not found in " + os.getcwd())
shutil.copy('index.html', 'index.html.bak')
t = open('index.html', encoding='utf-8').read()

if S in t and E in t:
    t = re.sub(re.escape(S) + '.*?' + re.escape(E), lambda m: block, t, flags=re.S)
elif '</body>' in t:
    t = t.replace('</body>', block + '\n</body>', 1)
else:
    t += '\n' + block + '\n'

open('index.html', 'w', encoding='utf-8').write(t)
print(" -> [SUCCESS] Inserted %d commits into index.html (backup: index.html.bak)" % len(log.split('\n')))
