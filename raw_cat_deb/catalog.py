import os, time, hashlib, html, shutil

EXTS = {'.img','.bin','.iso','.deb','.zip','.tar','.gz','.xz','.rom','.dsk','.flp'}
ROOTS = [os.getcwd(), os.path.expanduser('~/oeneye'), '/storage/emulated/0/Download']
SKIP = ('/.git/', '/Android/', '/.cache/')
HERE = os.path.dirname(os.path.abspath(__file__))

def fp(path):
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            h.update(f.read(1 << 20))
    except Exception:
        return '-'
    return h.hexdigest()[:16]

def human(n):
    if n < 1024:
        return "%d B" % n
    for u in ('KiB', 'MiB', 'GiB'):
        n /= 1024.0
        if n < 1024 or u == 'GiB':
            return "%.1f %s" % (n, u)

rows, seen, prints = [], set(), {}
print(" -> Scanning storage tree...")
for root in dict.fromkeys(os.path.realpath(r) for r in ROOTS if os.path.isdir(r)):
    for d, _, files in os.walk(root):
        if any(s in d + '/' for s in SKIP):
            continue
        for name in files:
            if os.path.splitext(name)[1].lower() not in EXTS:
                continue
            rp = os.path.realpath(os.path.join(d, name))
            if rp in seen or not os.path.isfile(rp):
                continue
            seen.add(rp)
            try:
                st = os.stat(rp)
            except Exception:
                continue
            key = (st.st_size, fp(rp))
            dup = key in prints
            prints.setdefault(key, rp)
            print(" -> %s %s" % ('Duplicate' if dup else 'Cataloging', name))
            rows.append((name, rp, st.st_size, st.st_mtime, key[1], dup))

rows.sort(key=lambda r: r[0].lower())
tr = ""
for name, p, size, mt, f, dup in rows:
    tr += "<tr class='%s'><td>%s</td><td>%s</td><td data-v='%d'>%s</td><td>%s</td><td><code>%s</code></td><td>%s</td></tr>\n" % (
        'dup' if dup else '', html.escape(name), html.escape(os.path.dirname(p)),
        size, human(size), time.strftime('%Y-%m-%d %H:%M', time.localtime(mt)),
        f, 'duplicate' if dup else 'unique')

tpl = open(os.path.join(HERE, 'catalog_tpl.html'), encoding='utf-8').read()
page = (tpl.replace('__DATE__', time.strftime('%Y-%m-%d %H:%M'))
           .replace('__N__', str(len(rows)))
           .replace('__U__', str(sum(1 for r in rows if not r[5])))
           .replace('__ROWS__', tr))

open('catalog.html', 'w', encoding='utf-8').write(page)
try:
    shutil.copy('catalog.html', '/storage/emulated/0/Download/catalog.html')
    print("\n -> [SUCCESS] Catalog generated at /storage/emulated/0/Download/catalog.html")
except Exception:
    print("\n -> [SUCCESS] Catalog generated at", os.path.abspath('catalog.html'))
