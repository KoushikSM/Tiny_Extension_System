import json, os, re, sys

EXT_DIR = sys.argv[1] if len(sys.argv) > 1 else 'tiny-extension'

# simple patterns to flag
SUSPICIOUS = [
    r'\beval\s*\(',
    r'new\s+Function\s*\(',
    r'document\.write\s*\(',
    r'\bsetTimeout\s*\(\s*["\']',
    r'XMLHttpRequest',
    r'\bfetch\s*\(',
    r'atob\s*\(',
    r'fromCharCode'
]

def scan_manifest(path):
    rep = {'permissions': [], 'host_permissions': [], 'all_urls': False, 'error': None}
    try:
        with open(path, encoding='utf-8') as f:
            m = json.load(f)
        perms = m.get('permissions', []) or []
        host = m.get('host_permissions', []) or []
        rep['permissions'] = perms
        rep['host_permissions'] = host
        rep['all_urls'] = ('<all_urls>' in perms) or ('<all_urls>' in host)
    except Exception as e:
        rep['error'] = str(e)
    return rep

def scan_files(root):
    hits = []
    for sub, _, files in os.walk(root):
        for fn in files:
            if fn.endswith(('.js', '.html')):
                p = os.path.join(sub, fn)
                try:
                    t = open(p, encoding='utf-8', errors='ignore').read()
                except:
                    t = ''
                for pat in SUSPICIOUS:
                    if re.search(pat, t):
                        hits.append((p, pat))
    return hits

if __name__ == '__main__':
    man = os.path.join(EXT_DIR, 'manifest.json')
    if not os.path.exists(man):
        print('No manifest.json found in', EXT_DIR)
        sys.exit(1)
    m = scan_manifest(man)
    if m['error']:
        print('Manifest parse error:', m['error'])
    print('Manifest permissions:', m['permissions'])
    print('Manifest host_permissions:', m['host_permissions'])
    print('Contains <all_urls>?:', m['all_urls'])
    findings = scan_files(EXT_DIR)
    if findings:
        print('Suspicious matches found:')
        for p, pat in findings:
            print('-', p, 'matches', pat)
    else:
        print('No suspicious patterns found (with this small rule set).')