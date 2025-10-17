# FLUID Documentation Generator

This document explains how the `generate-docs.py` script works to automatically generate HTML documentation from FLUID JSON schema files.

## Overview

The FLUID documentation generator is a Python script that:
1. Discovers JSON schema files in the project
2. Identifies the latest schema version
3. Generates beautiful HTML documentation using `json-schema-for-humans`
4. Outputs documentation to a versioned directory structure

## Prerequisites

- Python 3.6+ (tested with Python 3.12)
- Virtual environment (recommended)
- `json-schema-for-humans` package

### Installing Dependencies

```bash
# Activate your virtual environment
source .venv/bin/activate

# Install the required package
pip install json-schema-for-humans
```

## How It Works

### 1. Schema Discovery

The generator automatically discovers schema files in the `schema/` directory:

```python
def find_schema_files():
    candidates = list(SCHEMA_DIR.glob("fluid-schema-*.json"))
```

**Expected naming pattern**: `fluid-schema-X.Y.Z.json` where X.Y.Z is the semantic version.

**Example files**:
- `fluid-schema-0.1.0.json`
- `fluid-schema-0.5.7.json`
- `fluid-schema-1.0.0.json`

### 2. Version Extraction and Sorting

The script extracts version numbers using regex and sorts them semantically:

```python
def extract_version(filename: Path) -> str:
    match = re.search(r"(\d+\.\d+\.\d+)", filename.name)
    return match.group(1)
```

**Sorting logic**: Files are sorted by semantic version (e.g., 0.1.0 < 0.5.7 < 1.0.0), and the **latest version** is automatically selected for documentation generation.

### 3. Documentation Generation

The script uses the `json-schema-for-humans` library to convert JSON schemas into readable HTML documentation:

```python
def generate_docs(schema_file: Path, version: str):
    cmd = [
        str(venv_path),  # Path to generate-schema-doc in venv
        str(schema_file),
        str(output_file),
        "--config",
        "default"
    ]
```

**Key features**:
- Uses the `default` configuration for clean, readable output
- Automatically copies CSS and JavaScript assets
- Generates self-contained HTML files

### 4. Output Structure

Documentation is generated in a versioned directory structure:

```
specs/
├── 0.5.7/
│   ├── fluid-spec.html     # Main documentation
│   ├── schema_doc.css      # Styling
│   └── schema_doc.min.js   # Interactive features
├── 0.6.0/
│   ├── fluid-spec.html
│   ├── schema_doc.css
│   └── schema_doc.min.js
└── ...
```

## Directory Structure

The generator relies on this project structure:

```
fluid/
├── generate-docs.py        # The generator script
├── schema/                 # Source schema files
│   ├── fluid-schema-0.1.0.json
│   ├── fluid-schema-0.5.7.json
│   └── ...
└── specs/                  # Generated documentation
    ├── 0.5.7/
    ├── 0.6.0/
    └── ...
```

## Usage

### Basic Usage

Run the generator from the project root:

```bash
# Using the virtual environment Python
/path/to/.venv/bin/python generate-docs.py

# Or if virtual environment is activated
python generate-docs.py
```

### Example Output

```
[fluid-docs] Looking for schema files in: /path/to/schema
[fluid-docs] Found 7 schema files.
[fluid-docs]   - fluid-schema-0.1.1.json
[fluid-docs]   - fluid-schema-0.3.0.json
[fluid-docs]   - fluid-schema-0.5.7.json
[fluid-docs]   - ...
[fluid-docs] Using schema: fluid-schema-0.5.7.json (version 0.5.7)
[fluid-docs] Running command: generate-schema-doc ...
[fluid-docs] ✅ Docs generated at: /path/to/specs/0.5.7/fluid-spec.html
```

## Configuration

The generator currently uses the `default` configuration from `json-schema-for-humans`. This can be customized by:

1. **Modifying the config parameter**:
   ```python
   cmd = [..., "--config", "custom_config_name"]
   ```

2. **Using a config file**:
   ```python
   cmd = [..., "--config-file", "path/to/config.json"]
   ```

3. **Inline configuration**:
   ```python
   cmd = [..., "--config", "minify=false", "--config", "expand_buttons=true"]
   ```

## Key Features

### Robust Path Resolution
- All paths are resolved relative to the script location, not the current working directory
- Works regardless of where you run the script from

### Error Handling
- Graceful handling of missing dependencies
- Clear error messages with actionable advice
- Validation of schema file naming conventions

### Logging
- Detailed console output for debugging
- File and folder context in all messages
- Clear success/failure indicators

### Virtual Environment Support
- Automatically uses the correct Python environment
- Resolves the `generate-schema-doc` command path within the virtual environment

## Troubleshooting

### Common Issues

1. **"generate-schema-doc command not found"**
   - Install `json-schema-for-humans`: `pip install json-schema-for-humans`
   - Ensure you're using the correct Python environment

2. **"No schema files found"**
   - Check that files are in the `schema/` directory
   - Verify naming follows `fluid-schema-X.Y.Z.json` pattern

3. **Permission errors**
   - Ensure the `specs/` directory is writable
   - Check file permissions on schema files

### Debug Mode

For additional debugging, you can modify the script to add more verbose logging:

```python
def log(msg: str):
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [fluid-docs] {msg}")
```

## Extending the Generator

### Adding New Output Formats

The generator can be extended to support additional output formats by modifying the `generate_docs` function:

```python
def generate_docs(schema_file: Path, version: str, format_type="html"):
    if format_type == "html":
        # Current HTML generation
    elif format_type == "markdown":
        # Add markdown generation
    elif format_type == "pdf":
        # Add PDF generation
```

### Custom Schema Processing

You can add custom schema processing before documentation generation:

```python
def preprocess_schema(schema_file: Path) -> Path:
    # Load, modify, and save schema
    # Return path to processed schema
    pass
```

## Integration with CI/CD

The generator can be integrated into automated workflows:

```yaml
# GitHub Actions example
- name: Generate Documentation
  run: |
    source .venv/bin/activate
    python generate-docs.py
    
- name: Deploy Documentation
  # Upload or commit generated docs
```

## Dependencies

- **Python 3.6+**: Core runtime
- **json-schema-for-humans**: Documentation generation
- **pathlib**: Path handling (built-in)
- **subprocess**: Command execution (built-in)
- **re**: Regular expressions (built-in)

## License

This generator follows the same license as the FLUID project.