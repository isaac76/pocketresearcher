#!/usr/bin/python3

"""
Filter Memory Utility - Clean up the current memory.json file
"""

import json
import os
from datetime import datetime

# Handle imports
try:
    from .memory import Memory
    from .content_filter import ContentFilter
except ImportError:
    from memory import Memory
    from content_filter import ContentFilter

def filter_current_memory():
    """Filter the current memory.json file and create a cleaned version"""
    
    print("🧹 Starting content filtering process...")
    
    # Initialize components
    memory_store = Memory()
    content_filter = ContentFilter()
    
    # Load current memory
    print("📖 Loading current memory...")
    current_memory = memory_store.load()
    
    print(f"Current memory contains:")
    print(f"  - Facts: {len(current_memory.get('facts', []))}")
    print(f"  - Ideas: {len(current_memory.get('ideas', []))}")
    print(f"  - Proofs: {len(current_memory.get('proofs', []))}")
    print(f"  - Reflections: {len(current_memory.get('reflections', []))}")
    print(f"  - Formal Proofs: {len(current_memory.get('formal_proofs', []))}")
    print(f"  - Experiments: {len(current_memory.get('experiments', []))}")
    
    # Create backup
    backup_path = f"memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    print(f"💾 Creating backup: {backup_path}")
    
    with open(backup_path, 'w') as backup_file:
        json.dump(current_memory, backup_file, indent=2)
    
    # Apply filtering
    print("🔍 Applying content filters...")
    cleaned_memory, filter_log = content_filter.filter_memory(current_memory)
    
    # Update metadata
    cleaned_memory["metadata"] = {
        "topic": "P vs NP research",
        "last_updated": datetime.now().isoformat(),
        "last_filtered": datetime.now().isoformat(),
        "total_facts": len(cleaned_memory.get("facts", [])),
        "total_ideas": len(cleaned_memory.get("ideas", [])),
        "total_reflections": len(cleaned_memory.get("reflections", [])),
        "filtering_applied": True
    }
    
    # Save cleaned memory
    print("💾 Saving cleaned memory...")
    memory_store.save(cleaned_memory)
    
    # Save filter log
    filter_log_path = f"filter_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filter_log_path, 'w') as log_file:
        json.dump(filter_log, log_file, indent=2)
    
    # Generate and display report
    report = content_filter.generate_filter_report(filter_log)
    print(report)
    
    print(f"✅ Filtering complete!")
    print(f"📁 Backup saved to: {backup_path}")
    print(f"📁 Filter log saved to: {filter_log_path}")
    
    print(f"\nCleaned memory contains:")
    print(f"  - Facts: {len(cleaned_memory.get('facts', []))}")
    print(f"  - Ideas: {len(cleaned_memory.get('ideas', []))}")
    print(f"  - Proofs: {len(cleaned_memory.get('proofs', []))}")
    print(f"  - Reflections: {len(cleaned_memory.get('reflections', []))}")
    print(f"  - Formal Proofs: {len(cleaned_memory.get('formal_proofs', []))} (unchanged)")
    print(f"  - Experiments: {len(cleaned_memory.get('experiments', []))} (unchanged)")
    
    return cleaned_memory, filter_log

if __name__ == "__main__":
    filter_current_memory()
