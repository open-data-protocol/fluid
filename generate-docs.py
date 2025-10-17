#!/usr/bin/env python3
"""
generate-docs.py
----------------
A robust FLUID schema doc generator.

Improvements:
- Resolves schema directory relative to script location, not cwd
- Better console logging with file/folder context
- Graceful exception handling
- Clearer output for debugging
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# Resolve paths relative to this script file
SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_DIR = SCRIPT_DIR / "schema"
SPECS_DIR = SCRIPT_DIR / "specs"

def log(msg: str):
    """Simple logger"""
    print(f"[fluid-docs] {msg}")

def find_schema_files():
    """Find all schema files in ./schema/ matching fluid-schema-x.x.x.json"""
    log(f"Looking for schema files in: {SCHEMA_DIR}")
    if not SCHEMA_DIR.exists():
        log("❌ Schema directory does not exist.")
        return []

    candidates = list(SCHEMA_DIR.glob("fluid-schema-*.json"))
    log(f"Found {len(candidates)} schema files.")
    for c in candidates:
        log(f"  - {c.name}")
    return candidates

def extract_version(filename: Path) -> str:
    """Extract version x.x.x from schema filename"""
    match = re.search(r"(\d+\.\d+\.\d+)", filename.name)
    if not match:
        raise ValueError(f"Could not extract version from filename: {filename}")
    return match.group(1)

def generate_docs(schema_file: Path, version: str):
    """Run json-schema-for-humans to generate docs"""
    output_dir = SPECS_DIR / version
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "fluid-spec.html"

    # Use the full path to the generate-schema-doc command in the virtual environment
    venv_path = Path(__file__).resolve().parent.parent / ".venv" / "bin" / "generate-schema-doc"
    
    cmd = [
        str(venv_path),
        str(schema_file),
        str(output_file),
        "--config",
        "default"
    ]

    log(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        log("❌ Error: `generate-schema-doc` command not found. Did you install json-schema-for-humans?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        log(f"❌ Error running generate-schema-doc: {e}")
        sys.exit(1)

    log(f"✅ Docs generated at: {output_file}")

def main():
    try:
        candidates = find_schema_files()
        if not candidates:
            log("❌ No schema files found. Make sure they are in ./schema/ and named like fluid-schema-x.x.x.json")
            sys.exit(1)

        # Sort by version number
        def version_key(f):
            try:
                return tuple(map(int, extract_version(f).split(".")))
            except Exception:
                return (0,0,0)

        candidates.sort(key=version_key)
        latest = candidates[-1]
        version = extract_version(latest)

        log(f"Using schema: {latest.name} (version {version})")
        generate_docs(latest, version)

    except Exception as e:
        log(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
