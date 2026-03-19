#!/usr/bin/env python3
"""
VUC-2026 Pydantic Issues Fix Script
Fixes all 'any' vs 'Any' type annotation issues across the codebase
"""

import os
import re
from pathlib import Path

def fix_pydantic_issues():
    """Fix all Pydantic type annotation issues"""
    
    # Get all Python files in the app directory
    app_dir = Path("app")
    python_files = list(app_dir.rglob("*.py"))
    
    fixes_made = 0
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix 1: Add Any to imports if needed and Dict[str, any] is present
            if 'Dict[str, any]' in content and 'from typing import' in content and 'Any' not in content:
                # Add Any to existing typing import
                import_line = re.search(r'from typing import ([^\n]+)', content)
                if import_line:
                    current_imports = import_line.group(1)
                    if 'Any' not in current_imports:
                        new_imports = f'Any, {current_imports}'
                        content = content.replace(import_line.group(0), f'from typing import {new_imports}')
            
            # Fix 2: Replace Dict[str, any] with Dict[str, Any]
            content = re.sub(r'Dict\[str, any\]', 'Dict[str, Any]', content)
            
            # Fix 3: Replace List[any] with List[Any]
            content = re.sub(r'List\[any\]', 'List[Any]', content)
            
            # Fix 4: Replace Optional[any] with Optional[Any]
            content = re.sub(r'Optional\[any\]', 'Optional[Any]', content)
            
            # Fix 5: Replace Union[any, ...] with Union[Any, ...]
            content = re.sub(r'Union\[any,', 'Union[Any,', content)
            
            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixes_made += 1
                print(f"Fixed: {file_path}")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nTotal files fixed: {fixes_made}")
    return fixes_made

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    fix_pydantic_issues()
