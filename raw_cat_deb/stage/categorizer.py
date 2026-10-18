#!/usr/bin/env python3
"""categorizer.py - sort disk images and .deb packages into folders.
usage: categorizer.py [SRC] [--dest DIR] [--ext .raw,.img,...] [--copy] [--dry-run] [--max-mb N]
default: SRC=/storage/emulated/0/Download, files are MOVED inside SRC."""
import argparse
import os
import re
import shutil

VERSION = re.compile(r'(?<![A-Za-z0-9])(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?|bookworm|bullseye|trixie|forky|focal|jammy|noble|plucky)(?![A-Za-z0-9])', re.I)
ARCH = re.compile(r'_(amd64|arm64|armhf|armel|i386|riscv64|ppc64el|s390x|all)\.deb$', re.I)


def os_and_version(name):
    low = name.lower()
    if 'ubuntu' in low:
        os_type = 'Ubuntu'
    elif 'debian' in low:
        os_type = 'Debian'
    elif low.startswith('mosfetq'):
        os_type = 'MOSFETQ_DOS'
    elif '86-dos' in low:
        os_type = '86-DOS'
    elif 'oeneye' in low:
        os_type = 'oeneyeOS'
    else:
        os_type = 'Other_OS'
    m = VERSION.search(low)
    return os_type, (m.group(1) if m else 'Unknown_Version')


def target(name):
    if name.lower().endswith('.deb'):
        m = ARCH.search(name)
        return os.path.join('deb', m.group(1).lower() if m else 'unknown_arch')
    o, v = os_and_version(name)
    return os.path.join(o, v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src', nargs='?', default='/storage/emulated/0/Download')
    ap.add_argument('--dest')
    ap.add_argument('--ext', default='.raw,.img,.qcow2,.iso,.deb')
    ap.add_argument('--copy', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--max-mb', type=float, default=0)
    a = ap.parse_args()
    dest = a.dest or a.src
    exts = tuple(e.strip().lower() for e in a.ext.split(',') if e.strip())
    if not os.path.isdir(a.src):
        print('no such directory:', a.src)
        return 1
    n = big = 0
    for name in sorted(os.listdir(a.src)):
        path = os.path.join(a.src, name)
        if not os.path.isfile(path) or not name.lower().endswith(exts):
            continue
        mb = os.path.getsize(path) / 1048576
        if a.max_mb and mb > a.max_mb:
            print('skip (%d MB > %g MB): %s' % (mb, a.max_mb, name))
            big += 1
            continue
        folder = os.path.join(dest, target(name))
        out = os.path.join(folder, name)
        if os.path.exists(out):
            print('skip (exists):', out)
            continue
        if a.dry_run:
            verb = 'would copy' if a.copy else 'would move'
        else:
            os.makedirs(folder, exist_ok=True)
            (shutil.copy2 if a.copy else shutil.move)(path, out)
            verb = 'copied' if a.copy else 'moved'
        print(verb + ':', name, '->', os.path.relpath(folder, dest))
        n += 1
    print('%d file(s), %d skipped as too big' % (n, big))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
