#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline self-check of the generated corpus (no network):
 - data/projects/*.json parse, satisfy docs/schema.json (jsonschema if installed, else a stdlib fallback)
 - index.json / scorecard.csv agree with the per-project files
 - every project has a matching .md
Run: python3 tools/check_schema.py
"""
import csv, glob, io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(io.open(os.path.join(ROOT, "docs", "schema.json"), encoding="utf-8"))


def fallback_validate(obj, schema, path="$"):
    """Tiny draft-07 subset: type, required, properties, items, enum, minItems, minLength, pattern, ranges."""
    errs = []
    t = schema.get("type")
    types = {"string": str, "number": (int, float), "integer": int, "boolean": bool,
             "array": list, "object": dict, "null": type(None)}
    if t:
        allowed = [types[x] for x in (t if isinstance(t, list) else [t])]
        if allowed and not isinstance(obj, tuple(allowed)):
            errs.append(f"{path}: expected {t}, got {type(obj).__name__}")
            return errs
    if isinstance(obj, dict):
        for k in schema.get("required", []):
            if k not in obj:
                errs.append(f"{path}.{k}: required key missing")
        for k, v in (schema.get("properties") or {}).items():
            if k in obj:
                errs += fallback_validate(obj[k], v, f"{path}.{k}")
        if schema.get("additionalProperties") is False:
            extra = set(obj) - set((schema.get("properties") or {}).keys())
            if extra:
                errs.append(f"{path}: unexpected keys {sorted(extra)}")
    if isinstance(obj, list):
        if "minItems" in schema and len(obj) < schema["minItems"]:
            errs.append(f"{path}: needs >= {schema['minItems']} items, has {len(obj)}")
        if schema.get("items"):
            for i, it in enumerate(obj):
                errs += fallback_validate(it, schema["items"], f"{path}[{i}]")
    if isinstance(obj, str):
        if "minLength" in schema and len(obj) < schema["minLength"]:
            errs.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and __import__("re").search(schema["pattern"], obj) is None:
            errs.append(f"{path}: pattern {schema['pattern']!r} not matched")
    if "enum" in schema and obj not in schema["enum"]:
        errs.append(f"{path}: {obj!r} not in enum {schema['enum']}")
    for lo, key in (("minimum", "max"), ("maximum", "min")):
        pass
    if "minimum" in schema and isinstance(obj, (int, float)) and obj < schema["minimum"]:
        errs.append(f"{path}: {obj} < minimum {schema['minimum']}")
    if "maximum" in schema and isinstance(obj, (int, float)) and obj > schema["maximum"]:
        errs.append(f"{path}: {obj} > maximum {schema['maximum']}")
    return errs


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "data", "projects", "*.json")))
    if len(files) != 8:
        print(f"FAIL: expected 8 project JSON files, found {len(files)}")
        return 1
    try:
        import jsonschema  # type: ignore
        have = True
    except Exception:
        have = False
    ver = ''
    if have:
        try:
            from importlib.metadata import version; ver = ' ' + version('jsonschema')
        except Exception: pass
    print(f'validator: {"jsonschema" + ver if have else "stdlib fallback (jsonschema not installed)"}')
    bad = 0
    slugs = []
    for f in files:
        obj = json.load(io.open(f, encoding="utf-8"))
        errs = (list(e.message for e in jsonschema.Draft7Validator(SCHEMA).iter_errors(obj))
                if have else fallback_validate(obj, SCHEMA))
        name = os.path.basename(f)
        if errs:
            bad += 1
            print(f"FAIL {name}: {len(errs)} schema error(s)")
            for e in errs[:5]:
                print("   -", e)
        md = f[:-5] + ".md"
        if not os.path.exists(md):
            bad += 1; print(f"FAIL {name}: companion markdown missing")
        slugs.append(obj["slug"])
    idx = json.load(io.open(os.path.join(ROOT, "data", "index.json"), encoding="utf-8"))
    if [p["slug"] for p in idx["projects"]] != sorted(slugs) and sorted(p["slug"] for p in idx["projects"]) != sorted(slugs):
        bad += 1; print("FAIL index.json slugs disagree with project files")
    rows = list(csv.reader(io.open(os.path.join(ROOT, "data", "scorecard.csv"), encoding="utf-8-sig")))
    if len(rows) != 9:
        bad += 1; print(f"FAIL scorecard.csv: expected header + 8 rows, got {len(rows)}")
    elif sorted(r[1] for r in rows[1:]) != sorted(slugs):
        bad += 1; print("FAIL scorecard.csv slugs disagree with project files")
    if len(idx["fields_per_project"]) != 10:
        bad += 1; print("FAIL index.json: fields_per_project must list the 10 mandatory fields")
    for p in idx["projects"]:
        for k in ("slug", "rank", "interest", "credibility", "verdict_short", "json", "md", "needs_recheck"):
            if k not in p:
                bad += 1; print(f"FAIL index.json {p.get('slug')}: missing {k}")
    print(("OK: 8 records, 10 mandatory fields present, schema-valid, index/csv in sync"
            if not bad else f"{bad} problem(s) found"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
