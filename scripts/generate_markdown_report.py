#!/usr/bin/env python3
"""Generate a markdown report from the JSON produced by list_extensions.py"""
import json, argparse, textwrap
def summarize_chrome(chrome_entries):
    out = []
    for p in chrome_entries:
        out.append('## Chrome profile: %s\n' % p.get('profile_path'))
        exts = p.get('extensions', [])
        out.append('| ID | Name | Version(s) | Permissions |') 
        out.append('|----|------|------------|-------------|')
        for e in exts:
            id_ = e.get('id')
            names = []
            versions = []
            perms = set()
            for v in e.get('versions', []):
                m = v.get('manifest', {})
                names.append(m.get('name') or '')
                versions.append(m.get('version') or v.get('version_folder'))
                for p in (m.get('permissions') or []):
                    perms.add(str(p))
            out.append('| %s | %s | %s | %s |' % (
                id_,
                ', '.join([n for n in names if n])[:80].replace('\n',' '),
                ', '.join(versions),
                ', '.join(list(perms))[:200].replace('\n',' ')
            ))
        out.append('\n')
    return '\n'.join(out)

def summarize_firefox(ff_entries):
    out = []
    for p in ff_entries:
        out.append('## Firefox profile: %s\n' % p.get('profile_path'))
        out.append('| ID | Name | Version | Active | UserDisabled |')
        out.append('|----|------|---------|--------|--------------|')
        for a in p.get('addons', []):
            out.append('| %s | %s | %s | %s | %s |' % (
                a.get('id'),
                (a.get('name') or '')[:60],
                a.get('version'),
                a.get('active'),
                a.get('userDisabled')
            ))
        out.append('\n')
    return '\n'.join(out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', '-i', dest='infile', default='extensions.json')
    parser.add_argument('--out', '-o', dest='outfile', default='report.md')
    args = parser.parse_args()
    data = json.load(open(args.infile, encoding='utf-8'))
    parts = []
    parts.append('# Browser Extension Audit Report\n')
    parts.append('Generated from %s\n' % args.infile)
    if data.get('chrome'):
        parts.append(summarize_chrome(data.get('chrome')))
    if data.get('firefox'):
        parts.append(summarize_firefox(data.get('firefox')))
    open(args.outfile, 'w', encoding='utf-8').write('\n'.join(parts))
    print('Wrote', args.outfile)

if __name__ == '__main__':
    main()
