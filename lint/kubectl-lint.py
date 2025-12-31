#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
AUTHOR:         Nisharas / FixMyK8s
DATE:           2025-12-31
PURPOSE:        Universal K8s Linter & Healer.
                Refined to handle complex strings like image tags and URLs.
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
        with open(file_path, 'r') as f:
            original_content = f.read()

        # ---------------------------------------------------------
        # STEP 2: PRE-PROCESS (THE HEALER)
        # ---------------------------------------------------------

        # A. SMART COLON ADDER: Only add a colon if the line is exactly ONE keyword.
        # This prevents adding colons to values or comments.
        healed = re.sub(r'(^[ \t]*[\w.-]+)(?=[ \t]*$)', r'\1:', original_content, flags=re.MULTILINE)
        
        # B. IMAGE SHIELD: Find lines with 'image:' and a tag (multiple colons).
        # We wrap the value in quotes to protect it from the parser.
        # This fixes the 'paulbouwer/hello-kubernetes:1.8' error.
        healed = re.sub(r'(image:[ \t]*)([^"\s\n][^#\n]*:[^#\n]*)', r'\1"\2"', healed)

        # C. KEY-SPACE FIXER: Fix 'image:nginx' -> 'image: nginx'
        # We use a negative lookahead to ensure we only fix the FIRST colon after a key.
        healed = re.sub(r'(^[ \t]*[\w.-]+):(?!\s| )', r'\1: ', healed, flags=re.MULTILINE)
        
        # D. TAB TO SPACE: Standardize
        healed = healed.replace('\t', '  ')

        # ---------------------------------------------------------
        # STEP 3: NORMALIZE
        # ---------------------------------------------------------
        docs = list(yaml.load_all(healed))
        output_buffer = StringIO()
        yaml.dump_all(docs, output_buffer)
        healed_final = output_buffer.getvalue()

        # 4. Compare
        diff = list(difflib.unified_diff(
            original_content.splitlines(),
            healed_final.splitlines(),
            fromfile='Current',
            tofile='Healed',
            lineterm=''
        ))

        print(f"\n🩺 [DIAGNOSTIC REPORT] File: {file_path}")
        print("=" * 60)
        
        if not diff:
            print("✔ Manifest is already healthy. No changes required.")
        else:
            for line in diff:
                if line.startswith('+') and not line.startswith('+++'):
                    print(f"\033[92m{line}\033[0m")
                elif line.startswith('-') and not line.startswith('---'):
                    print(f"\033[91m{line}\033[0m")
            
            with open(file_path, 'w') as f:
                f.write(healed_final)
            
            print("=" * 60)
            print(f"SUCCESS: Configuration file '{file_path}' has been healed.")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] Auto-heal failed: {e}")
        print("TIP: If you have complex strings, try wrapping them in \"quotes\".")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("""
🩺 kubectl-lint: The K8s Manifest Healer

Usage:
  kubectl lint <filename.yaml>

What it fixes:
  - Missing colons on keys
  - Image tags with multiple colons (Auto-quoting)
  - Missing spaces after colons
  - Tabs and indentation issues
        """)
    else:
        linter_engine(sys.argv[1])
