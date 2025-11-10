#!/usr/bin/env python3
"""
Year Updater for The Code Master Project
Automatically updates copyright years in README and source files
"""

import os
from datetime import datetime

def update_year_in_file(filepath):
    """Update year in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get current year
        current_year = datetime.now().year
        
        # Check if file exists and needs update
        if '2024-2025' not in content and '2024' in content:
            # Update single year to range
            content = content.replace('2024', f'2024-{current_year}')
        elif f'2024-{current_year}' not in content:
            # Update existing range
            import re
            content = re.sub(r'2024-\d{4}', f'2024-{current_year}', content)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main function to update years in project files"""
    print("=" * 60)
    print("The Code Master - Year Updater")
    print("=" * 60)
    
    # Files to update
    files_to_update = [
        'README.md',
        'CODE_MASTER_README.md',
        'PROJECT_COMPLETION_SUMMARY.md',
        'ARCHITECTURE.md',
        'API_REFERENCE.md'
    ]
    
    updated_count = 0
    
    for filepath in files_to_update:
        if os.path.exists(filepath):
            if update_year_in_file(filepath):
                updated_count += 1
        else:
            print(f"⚠️  File not found: {filepath}")
    
    print("=" * 60)
    print(f"✅ Year update complete! Updated {updated_count} files.")
    print(f"© 2024-{datetime.now().year} | Developed by Duncan N. for Developers")
    print("=" * 60)

if __name__ == '__main__':
    main()
