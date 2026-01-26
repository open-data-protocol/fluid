#!/usr/bin/env python3
"""
generate-schema-diffs.py
------------------------
Generates human-readable diff files between consecutive versions of FLUID schemas.

Creates markdown files showing:
- New properties added
- Properties removed  
- Properties modified
- Value changes in a clear, readable format
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Resolve paths relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
SCHEMA_DIR = SCRIPT_DIR / "schema"
DIFFS_DIR = SCRIPT_DIR / "schema-diffs"


def log(msg: str):
    """Simple logger"""
    print(f"[schema-diff] {msg}")


def extract_version(filename: Path) -> str:
    """Extract version x.x.x from schema filename"""
    match = re.search(r"(\d+\.\d+\.\d+)", filename.name)
    if not match:
        raise ValueError(f"Could not extract version from: {filename}")
    return match.group(1)


def version_key(version_str: str) -> Tuple[int, int, int]:
    """Convert version string to sortable tuple"""
    return tuple(map(int, version_str.split(".")))


def find_schema_files() -> List[Tuple[str, Path]]:
    """Find all schema files and return sorted list of (version, path) tuples"""
    log(f"Looking for schema files in: {SCHEMA_DIR}")
    if not SCHEMA_DIR.exists():
        log("❌ Schema directory does not exist.")
        return []

    candidates = list(SCHEMA_DIR.glob("fluid-schema-*.json"))
    versions = [(extract_version(f), f) for f in candidates]
    versions.sort(key=lambda x: version_key(x[0]))
    
    log(f"Found {len(versions)} schema versions")
    return versions


def compare_dicts(old: Dict, new: Dict, path: str = "") -> Dict[str, List]:
    """
    Recursively compare two dictionaries and categorize changes.
    Returns dict with 'added', 'removed', 'modified' keys.
    """
    changes = {
        'added': [],
        'removed': [],
        'modified': []
    }
    
    old_keys = set(old.keys()) if isinstance(old, dict) else set()
    new_keys = set(new.keys()) if isinstance(new, dict) else set()
    
    # Find added keys
    for key in new_keys - old_keys:
        full_path = f"{path}.{key}" if path else key
        changes['added'].append((full_path, new[key]))
    
    # Find removed keys
    for key in old_keys - new_keys:
        full_path = f"{path}.{key}" if path else key
        changes['removed'].append((full_path, old[key]))
    
    # Find modified keys
    for key in old_keys & new_keys:
        full_path = f"{path}.{key}" if path else key
        old_val = old[key]
        new_val = new[key]
        
        # Both are dicts - recurse
        if isinstance(old_val, dict) and isinstance(new_val, dict):
            sub_changes = compare_dicts(old_val, new_val, full_path)
            changes['added'].extend(sub_changes['added'])
            changes['removed'].extend(sub_changes['removed'])
            changes['modified'].extend(sub_changes['modified'])
        # Both are lists - simple comparison
        elif isinstance(old_val, list) and isinstance(new_val, list):
            if old_val != new_val:
                changes['modified'].append((full_path, old_val, new_val))
        # Direct value comparison
        elif old_val != new_val:
            changes['modified'].append((full_path, old_val, new_val))
    
    return changes


def format_value(val: Any, indent: int = 0) -> str:
    """Format a value for display in markdown"""
    indent_str = "  " * indent
    
    if isinstance(val, dict):
        if not val:
            return "{}"
        lines = ["{"]
        for k, v in list(val.items())[:5]:  # Limit to first 5 items
            lines.append(f"{indent_str}  {k}: {format_value(v, indent + 1)}")
        if len(val) > 5:
            lines.append(f"{indent_str}  ... ({len(val) - 5} more)")
        lines.append(f"{indent_str}}}")
        return "\n".join(lines)
    elif isinstance(val, list):
        if not val:
            return "[]"
        if len(val) <= 3:
            return json.dumps(val)
        return f"[...{len(val)} items...]"
    elif isinstance(val, str) and len(val) > 100:
        return f'"{val[:100]}..."'
    else:
        return json.dumps(val)


def generate_diff_markdown(old_version: str, new_version: str, 
                          old_schema: Dict, new_schema: Dict) -> str:
    """Generate a markdown document showing the differences"""
    changes = compare_dicts(old_schema, new_schema)
    
    # Count changes
    total_changes = (len(changes['added']) + len(changes['removed']) + 
                    len(changes['modified']))
    
    md = [
        f"# Schema Changes: {old_version} → {new_version}",
        "",
        f"**Total changes:** {total_changes}",
        f"- ✅ Added: {len(changes['added'])}",
        f"- ❌ Removed: {len(changes['removed'])}",
        f"- 📝 Modified: {len(changes['modified'])}",
        "",
        "---",
        ""
    ]
    
    # Added properties
    if changes['added']:
        md.append("## ✅ Added Properties")
        md.append("")
        for path, value in sorted(changes['added']):
            md.append(f"### `{path}`")
            md.append("```json")
            md.append(format_value(value))
            md.append("```")
            md.append("")
    
    # Removed properties
    if changes['removed']:
        md.append("## ❌ Removed Properties")
        md.append("")
        for path, value in sorted(changes['removed']):
            md.append(f"### `{path}`")
            md.append("```json")
            md.append(format_value(value))
            md.append("```")
            md.append("")
    
    # Modified properties
    if changes['modified']:
        md.append("## 📝 Modified Properties")
        md.append("")
        for item in sorted(changes['modified'], key=lambda x: x[0]):
            path = item[0]
            old_val = item[1]
            new_val = item[2]
            
            md.append(f"### `{path}`")
            md.append("")
            md.append("**Before:**")
            md.append("```json")
            md.append(format_value(old_val))
            md.append("```")
            md.append("")
            md.append("**After:**")
            md.append("```json")
            md.append(format_value(new_val))
            md.append("```")
            md.append("")
    
    # No changes
    if total_changes == 0:
        md.append("## No Changes Detected")
        md.append("")
        md.append("The schemas appear to be identical.")
        md.append("")
    
    return "\n".join(md)


def generate_diff(old_version: str, old_path: Path, 
                 new_version: str, new_path: Path):
    """Generate a diff file between two schema versions"""
    
    # Load schemas
    with open(old_path, 'r', encoding='utf-8') as f:
        old_schema = json.load(f)
    
    with open(new_path, 'r', encoding='utf-8') as f:
        new_schema = json.load(f)
    
    # Generate markdown
    markdown = generate_diff_markdown(old_version, new_version, old_schema, new_schema)
    
    # Write to file
    output_file = DIFFS_DIR / f"diff-{old_version}-to-{new_version}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    log(f"✅ Generated: {output_file.name}")


def generate_index(versions: List[Tuple[str, Path]]):
    """Generate an index file listing all diffs"""
    md = [
        "# FLUID Schema Version History",
        "",
        "This directory contains human-readable diffs between consecutive versions of the FLUID schema.",
        "",
        "## Version Progression",
        ""
    ]
    
    for i in range(len(versions) - 1):
        old_ver = versions[i][0]
        new_ver = versions[i + 1][0]
        md.append(f"- [{old_ver} → {new_ver}](diff-{old_ver}-to-{new_ver}.md)")
    
    md.append("")
    md.append("---")
    md.append("")
    md.append(f"**Versions tracked:** {len(versions)}")
    md.append(f"**Diff files generated:** {len(versions) - 1}")
    md.append("")
    
    index_file = DIFFS_DIR / "README.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))
    
    log(f"✅ Generated index: {index_file.name}")


def main():
    """Main entry point"""
    log("Starting schema diff generation...")
    
    # Find all schema versions
    versions = find_schema_files()
    
    if len(versions) < 2:
        log("❌ Need at least 2 schema versions to generate diffs")
        return
    
    # Generate diffs for consecutive versions
    for i in range(len(versions) - 1):
        old_ver, old_path = versions[i]
        new_ver, new_path = versions[i + 1]
        
        log(f"Comparing {old_ver} -> {new_ver}")
        generate_diff(old_ver, old_path, new_ver, new_path)
    
    # Generate index
    generate_index(versions)
    
    log(f"✅ Complete! Generated {len(versions) - 1} diff files in {DIFFS_DIR}")


if __name__ == "__main__":
    main()
