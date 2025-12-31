#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
AUTHOR:         Your Name / GitHub Handle
DATE:           2025-12-31
PURPOSE:        Professional K8s Linter & Healer.
                Fixes syntax (Tabs/Spaces/Colons) and provides a visual report.
--------------------------------------------------------------------------------
"""
import sys
import re
import difflib
from io import StringIO
from ruamel.yaml import YAML

def linter_engine(file_path):
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True
    
    try:
        # 1. Read original manifest
        with open(file_path, 'r') as f:
            original_content = f.read()

        # 2. Pre-Process: Fix common 'un-parseable' YAML errors via Regex
        # Fix missing space after colon: 'image:nginx' -> 'image: nginx'
        healed = re.sub(r'(^[ \t]*[\w.-]+):(?!\s)', r'\1: ', original_content, flags=re.MULTILINE)
        # Fix illegal Tabs -> 2 Spaces
        healed = healed.replace('\t', '  ')

        # 3. Normalize: Load and re-dump to standardize indentation
        # load_all handles files with '---' separators
        docs = list(yaml.load_all(healed))
        output_buffer = StringIO()
        yaml.dump_all(docs, output_buffer)
        healed_final = output_buffer.getvalue()

        # 4. Compare for the Diagnostic Report
        diff = list(difflib.unified_diff(
            original_content.splitlines(),
            healed_final.splitlines(),
            fromfile='Current',
            tofile='Healed',
            lineterm=''
        ))

        # 5. UI Reporting
        print(f"\n🩺 [DIAGNOSTIC REPORT] File: {file_path}")
        print("=" * 60)
        
        if not diff:
            print("✔ Manifest is already healthy. No changes required.")
        else:
            for line in diff:
                if line.startswith('+') and not line.startswith('+++'):
                    print(f"\033[92m{line}\033[0m") # Green (Fixed)
                elif line.startswith('-') and not line.startswith('---'):
                    print(f"\033[91m{line}\033[0m") # Red (Error)
            
            # 6. Save the healed file
            with open(file_path, 'w') as f:
                f.write(healed_final)
            
            print("=" * 60)
            print(f"SUCCESS: Configuration file '{file_path}' has been healed.")
            print("STATUS: Ready for environment deployment.")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] Auto-heal failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("""
🩺 kubectl-lint: The K8s Manifest Healer

Usage:
  kubectl lint <filename.yaml>

Options:
  -h, --help    Show this help menu

What it fixes:
  - Converts tabs to 2 spaces
  - Fixes indentation for lists and keys
  - Adds missing spaces after colons (e.g. image:nginx -> image: nginx)
        """)
    else:
        # Your existing linter function call
        heal_manifest(sys.argv[1])
