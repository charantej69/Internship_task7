#!/usr/bin/env python3
"""Enumerate Chrome (Chromium/Brave/Edge) and Firefox extensions from local profiles.
Produces a JSON file with discovered extensions and basic metadata.

Notes:
- This script searches common profile locations on Windows, macOS and Linux.
- It reads manifest.json (Chrome) and addons.json (Firefox) when available.
- Run as the same user who uses the browser.
"""
import os, sys, json, argparse, platform, glob
from pathlib import Path

def find_chrome_profiles():
    system = platform.system()
    paths = []
    if system == 'Linux':
        base = Path.home() / '.config'
        candidates = ['google-chrome', 'chromium', 'brave', 'microsoft-edge']
        for c in candidates:
            p = base / c
            if p.exists():
                for profile in p.glob('**/Default') + p.glob('**/Profile*'):
                    pass
        # Simpler: search for Extensions directories
        for p in base.glob('**/Extensions'):
            paths.append(str(p.parent))
    elif system == 'Darwin':
        base = Path.home() / 'Library' / 'Application Support'
        for p in base.glob('**/Extensions'):
            paths.append(str(p.parent))
    elif system == 'Windows':
        local = os.environ.get('LOCALAPPDATA')
        if local:
            base = Path(local)
            for p in base.glob('**/Extensions'):
                paths.append(str(p.parent))
    # dedupe
    return sorted(set(paths))

def parse_chrome_extensions(profile_path):
    exts = []
    ext_dir = Path(profile_path) / 'Extensions'
    if not ext_dir.exists():
        return exts
    for ext_id in ext_dir.iterdir():
        if not ext_id.is_dir(): continue
        # versions inside
        versions = list(ext_id.iterdir())
        if not versions: continue
        # pick latest version folder (sorted by name)
        versions_sorted = sorted([v for v in versions if v.is_dir()], key=lambda p: p.name, reverse=True)
        manifest = versions_sorted[0] / 'manifest.json'
        data = {'id': ext_id.name, 'versions': []}
        for v in versions_sorted:
            m = v / 'manifest.json'
            if m.exists():
                try:
                    mm = json.loads(m.read_text(encoding='utf-8', errors='ignore'))
                    data['versions'].append({
                        'version_folder': v.name,
                        'manifest': {
                            'name': mm.get('name'),
                            'description': mm.get('description'),
                            'version': mm.get('version'),
                            'permissions': mm.get('permissions') or [],
                            'host_permissions': mm.get('host_permissions') or [],
                        }
                    })
                except Exception as e:
                    data['versions'].append({'version_folder': v.name, 'manifest_error': str(e)})
        exts.append(data)
    return exts

def find_firefox_profiles():
    system = platform.system()
    paths = []
    if system == 'Linux':
        base = Path.home() / '.mozilla' / 'firefox'
        if base.exists():
            for p in base.glob('*.default*'):
                paths.append(str(p))
    elif system == 'Darwin':
        base = Path.home() / 'Library' / 'Application Support' / 'Firefox' / 'Profiles'
        if base.exists():
            for p in base.glob('*'):
                paths.append(str(p))
    elif system == 'Windows':
        appdata = os.environ.get('APPDATA')
        if appdata:
            base = Path(appdata) / 'Mozilla' / 'Firefox' / 'Profiles'
            if base.exists():
                for p in base.glob('*'):
                    paths.append(str(p))
    return sorted(set(paths))

def parse_firefox_addons(profile_path):
    addons = []
    addons_json = Path(profile_path) / 'addons.json'
    if not addons_json.exists():
        return addons
    try:
        j = json.loads(addons_json.read_text(encoding='utf-8', errors='ignore'))
        for a in j.get('addons', []):
            addons.append({
                'id': a.get('id'),
                'name': a.get('defaultLocale', {}).get('name') or a.get('name'),
                'version': a.get('version'),
                'type': a.get('type'),
                'active': a.get('active'),
                'userDisabled': a.get('userDisabled'),
                'installDate': a.get('installDate'),
                'foreignInstall': a.get('foreignInstall'),
            })
    except Exception as e:
        return [{'error': str(e)}]
    return addons

def main():
    parser = argparse.ArgumentParser(description='Enumerate Chrome & Firefox extensions')
    parser.add_argument('--out', '-o', default='extensions.json', help='Output JSON file path')
    args = parser.parse_args()

    result = {'chrome': [], 'firefox': []}

    chrome_profiles = find_chrome_profiles()
    for p in chrome_profiles:
        try:
            exts = parse_chrome_extensions(p)
            if exts:
                result['chrome'].append({'profile_path': p, 'extensions': exts})
        except Exception as e:
            result['chrome'].append({'profile_path': p, 'error': str(e)})

    ff_profiles = find_firefox_profiles()
    for p in ff_profiles:
        try:
            addons = parse_firefox_addons(p)
            if addons:
                result['firefox'].append({'profile_path': p, 'addons': addons})
        except Exception as e:
            result['firefox'].append({'profile_path': p, 'error': str(e)})

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print('Wrote', args.out)

if __name__ == '__main__':
    main()
