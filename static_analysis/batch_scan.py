import os, json, re, csv, sys
from typing import List, Dict, Any
 
# ---- config --------------------------------------------------------------
 
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
 
# file extensions to scan for code/markup
SCAN_EXTS = ('.js', '.mjs', '.cjs', '.html', '.htm')
 
# -------------------------------------------------------------------------
 
def load_manifest(path: str) -> Dict[str, Any]:
    """
    Load manifest.json with utf-8-sig to be tolerant of BOM.
    Return {} if invalid.
    """
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        return {"__error__": str(e)}
 
def scan_files(root: str) -> Dict[str, int]:
    """Return counts of each suspicious pattern in all files under root."""
    counts = {p: 0 for p in SUSPICIOUS}
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith(SCAN_EXTS):
                p = os.path.join(dirpath, fn)
                try:
                    text = open(p, encoding='utf-8', errors='ignore').read()
                except Exception:
                    text = ""
                for pat in SUSPICIOUS:
                    if re.search(pat, text):
                        counts[pat] += 1
    return counts
 
def summarize_extension(ext_dir: str) -> Dict[str, Any]:
    """Summarize a single extension directory."""
    row: Dict[str, Any] = {
        "ext_path": ext_dir,
        "manifest_version": "",
        "permissions": "",
        "host_permissions": "",
        "has_all_urls": False,
        "manifest_error": "",
    }
    man_path = os.path.join(ext_dir, "manifest.json")
    if not os.path.exists(man_path):
        row["manifest_error"] = "manifest.json not found"
        return row
 
    m = load_manifest(man_path)
    if "__error__" in m:
        row["manifest_error"] = m["__error__"]
        return row
 
    row["manifest_version"] = m.get("manifest_version", "")
    perms = m.get("permissions", []) or []
    host = m.get("host_permissions", []) or []
    row["permissions"] = ";".join(perms)
    row["host_permissions"] = ";".join(host)
    row["has_all_urls"] = ("<all_urls>" in perms) or ("<all_urls>" in host)
 
    counts = scan_files(ext_dir)
    # flatten suspicious counts into columns
    for pat in SUSPICIOUS:
        safe_col = pat.replace('\\', '').replace('(', '').replace(')', '').replace('?', '').replace('*', '')
        row[f"count_{safe_col}"] = counts[pat]
    # total matches
    row["suspicious_total"] = sum(counts.values())
    return row
 
def main():
    # root containing many extension folders
    root = sys.argv[1] if len(sys.argv) > 1 else "samples"
    out_csv = sys.argv[2] if len(sys.argv) > 2 else "scan_results.csv"
 
    if not os.path.isdir(root):
        print(f"Root folder not found: {root}")
        sys.exit(1)
 
    # treat each immediate subfolder as an extension
    ext_dirs = []
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name)
        if os.path.isdir(p):
            ext_dirs.append(p)
 
    if not ext_dirs:
        print(f"No extension folders found under: {root}")
        sys.exit(1)
 
    rows = []
    for ext in ext_dirs:
        rows.append(summarize_extension(ext))
 
    # ensure consistent columns
    base_cols = [
        "ext_path", "manifest_version", "permissions", "host_permissions",
        "has_all_urls", "manifest_error"
    ]
    susp_cols = []
    for pat in SUSPICIOUS:
        safe_col = pat.replace('\\', '').replace('(', '').replace(')', '').replace('?', '').replace('*', '')
        susp_cols.append(f"count_{safe_col}")
    all_cols = base_cols + susp_cols + ["suspicious_total"]
 
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=all_cols)
        w.writeheader()
        for r in rows:
            # fill any missing columns (e.g., when manifest missing)
            for c in all_cols:
                if c not in r:
                    r[c] = ""
            w.writerow(r)
 
    # quick summary to terminal
    total = len(rows)
    with_all_urls = sum(1 for r in rows if r["has_all_urls"] in (True, "True"))
    any_suspicious = sum(1 for r in rows if str(r.get("suspicious_total", "0")) not in ("", "0"))
    print(f"Scanned {total} extension(s).")
    print(f" - With <all_urls>: {with_all_urls} ({with_all_urls/total:.0%})")
    print(f" - With any suspicious pattern: {any_suspicious} ({any_suspicious/total:.0%})")
    print(f"Wrote: {out_csv}")
 
if __name__ == "__main__":
    main()