#!/usr/bin/env python3
"""
PocketResearcher Cleanup Script
Safely removes unused files after unified configuration migration
"""

import os
import shutil
from datetime import datetime

def cleanup_project():
    """Clean up unused files after unified configuration migration"""
    
    print("🧹 PocketResearcher Project Cleanup")
    print("=" * 50)
    
    # Create archive directory for files we want to keep but not use
    archive_dir = "archive_legacy"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"📁 Created archive directory: {archive_dir}")
    
    # Files to delete (safe to remove)
    files_to_delete = [
        "memory-even-proof-contaminated-backup.json",
        "memory-test-contaminated.json", 
        "memory-even-proof.json.backup",
        "filter_log_20250811_150523.json"
    ]
    
    # Files to archive (keep for reference but not active)
    files_to_archive = [
        "config.py",
        "config.py.sample", 
        "src/p_vs_np.py",
        "src/direct_proof.py",
        "src/pocketresearcher.py",
        "pocketresearcher_unified.py",
        "demo_unified_config.py",
        "demo_solution.py",
        "research_log.md"
    ]
    
    # Optional files (ask user)
    optional_files = [
        "research_log_direct_proof.md",
        "research_log_p_vs_np.md"
    ]
    
    print("\n🗑️  DELETING TEMPORARY FILES:")
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"   ✅ Deleted: {file}")
        else:
            print(f"   ⚠️  Not found: {file}")
    
    print(f"\n📦 ARCHIVING LEGACY FILES TO {archive_dir}:")
    for file in files_to_archive:
        if os.path.exists(file):
            archive_path = os.path.join(archive_dir, os.path.basename(file))
            shutil.move(file, archive_path)
            print(f"   ✅ Archived: {file} → {archive_path}")
        else:
            print(f"   ⚠️  Not found: {file}")
    
    print(f"\n❓ OPTIONAL FILES (keep recent logs?):")
    for file in optional_files:
        if os.path.exists(file):
            response = input(f"   Keep {file}? (y/N): ").lower()
            if response != 'y':
                archive_path = os.path.join(archive_dir, os.path.basename(file))
                shutil.move(file, archive_path)
                print(f"   📦 Archived: {file}")
            else:
                print(f"   ✅ Kept: {file}")
    
    print(f"\n✨ CLEANUP COMPLETE!")
    print(f"\n📁 ACTIVE PROJECT STRUCTURE:")
    
    # Show clean project structure
    active_files = []
    for root, dirs, files in os.walk("."):
        # Skip .git, .venv, __pycache__, archive
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != archive_dir]
        
        for file in files:
            if not file.startswith('.') and not file.endswith('.pyc'):
                rel_path = os.path.relpath(os.path.join(root, file))
                if not rel_path.startswith(archive_dir):
                    active_files.append(rel_path)
    
    # Group by category
    core_files = [f for f in active_files if f.startswith('src/')]
    config_files = [f for f in active_files if 'config' in f or f.endswith('_v2.py')]
    memory_files = [f for f in active_files if f.startswith('memory-') and f.endswith('.json')]
    doc_files = [f for f in active_files if f.endswith('.md') or f.endswith('.txt') or f == 'LICENSE']
    other_files = [f for f in active_files if f not in core_files + config_files + memory_files + doc_files]
    
    print("\n   🔧 CORE SYSTEM:")
    for f in sorted(config_files):
        print(f"      {f}")
    
    print("\n   📚 SOURCE MODULES:")
    for f in sorted(core_files):
        print(f"      {f}")
    
    print("\n   💾 MEMORY FILES:")
    for f in sorted(memory_files):
        print(f"      {f}")
    
    print("\n   📋 DOCUMENTATION:")
    for f in sorted(doc_files):
        print(f"      {f}")
    
    if other_files:
        print("\n   📊 OTHER:")
        for f in sorted(other_files):
            print(f"      {f}")
    
    print(f"\n🎯 UNIFIED SYSTEM READY!")
    print(f"   Main command: python pocketresearcher_v2.py [problem] [llm]")
    print(f"   Configuration: config_unified.py")
    print(f"   Legacy files: {archive_dir}/")

if __name__ == "__main__":
    cleanup_project()
