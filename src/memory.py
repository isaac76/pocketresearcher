import os
import json
from typing import Optional, Dict, List, Any

# Optional imports for database support
try:
    import pymongo
except ImportError:
    pymongo = None
try:
    import memcache
except ImportError:
    memcache = None

class MemoryBackend:
    FILE = "file"
    MONGODB = "mongodb"
    MEMCACHED = "memcached"

class Memory:
    def __init__(self, config: Optional[dict] = None, category: str = None):
        self.backend = config.get("backend", MemoryBackend.FILE) if config else MemoryBackend.FILE
        self.category = category  # Current working category
        
        # Use configured file path or default to dictionary.json for unified storage
        if config and "file_path" in config:
            # If relative path, make it relative to project root
            configured_path = config["file_path"]
            if not os.path.isabs(configured_path):
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                self.file_path = os.path.join(project_root, configured_path)
            else:
                self.file_path = configured_path
        else:
            # Default to unified dictionary.json
            self.file_path = self._get_dictionary_path()
            
        self.mongo_uri = config.get("mongo_uri") if config else None
        self.mongo_db = config.get("mongo_db", "pocketresearcher") if config else "pocketresearcher"
        self.mongo_collection = config.get("mongo_collection", "memory") if config else "memory"
        self.memcached_host = config.get("memcached_host", "127.0.0.1:11211") if config else "127.0.0.1:11211"
        self._setup_backend()

    def _get_dictionary_path(self):
        """Get the correct path to dictionary.json regardless of execution context."""
        # Get the directory where this file (memory.py) is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to the project root and find dictionary.json
        project_root = os.path.dirname(current_dir)
        dictionary_path = os.path.join(project_root, "dictionary.json")
        return dictionary_path

    def _get_memory_path(self):
        """Get the correct path to memory.json regardless of execution context."""
        # Get the directory where this file (memory.py) is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level to the project root and find memory.json
        project_root = os.path.dirname(current_dir)
        memory_path = os.path.join(project_root, "memory.json")
        return memory_path

    def _setup_backend(self):
        if self.backend == MemoryBackend.MONGODB and pymongo:
            self.mongo_client = pymongo.MongoClient(self.mongo_uri)
            self.collection = self.mongo_client[self.mongo_db][self.mongo_collection]
        elif self.backend == MemoryBackend.MEMCACHED and memcache:
            self.mc = memcache.Client([self.memcached_host], debug=0)

    def load(self, category: str = None):
        """Load memory data, optionally for a specific category"""
        if self.backend == MemoryBackend.FILE:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    
                # Handle unified dictionary format
                if "categories" in data:
                    if category:
                        if category in data["categories"]:
                            return data["categories"][category]
                        else:
                            # Create empty category structure
                            empty_category = {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": [], "formal_proofs": []}
                            return empty_category
                    else:
                        # Return the entire dictionary structure
                        return data
                else:
                    # Legacy format - return as-is
                    return data
                    
            # Create empty dictionary if file doesn't exist
            empty_dict = {
                "categories": {}
            }
            if category:
                empty_dict["categories"][category] = {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": [], "formal_proofs": []}
                return empty_dict["categories"][category]
            return empty_dict
            
        elif self.backend == MemoryBackend.MONGODB and pymongo:
            doc_id = f"memory_{category}" if category else "memory"
            doc = self.collection.find_one({"_id": doc_id})
            if doc:
                return doc.get("data", {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": [], "formal_proofs": []})
            return {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": [], "formal_proofs": []}
            
        elif self.backend == MemoryBackend.MEMCACHED and memcache:
            cache_key = f"memory_{category}" if category else "memory"
            data = self.mc.get(cache_key)
            if data:
                return json.loads(data)
            return {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": [], "formal_proofs": []}
        else:
            raise RuntimeError("Unsupported backend or missing library")

    def save(self, memory, category: str = None):
        """Save memory data, optionally for a specific category"""
        if self.backend == MemoryBackend.FILE:
            # Load existing dictionary structure
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    full_data = json.load(f)
            else:
                full_data = {"categories": {}}
                
            # Ensure categories structure exists
            if "categories" not in full_data:
                full_data["categories"] = {}

            # Fallback to self.category if category not provided
            if category is None:
                category = self.category

            # If memory is already in unified format, save directly
            if "categories" in memory:
                full_data = memory
            else:
                # Legacy save - need to specify category
                if not category:
                    raise ValueError("Category must be specified when saving legacy format data")
                # Save to specific category
                full_data["categories"][category] = memory
                    
            # Write back to file
            with open(self.file_path, "w") as f:
                json.dump(full_data, f, indent=2)
                
        elif self.backend == MemoryBackend.MONGODB and pymongo:
            doc_id = f"memory_{category}" if category else "memory"
            self.collection.update_one({"_id": doc_id}, {"$set": {"data": memory}}, upsert=True)
            
        elif self.backend == MemoryBackend.MEMCACHED and memcache:
            cache_key = f"memory_{category}" if category else "memory"
            self.mc.set(cache_key, json.dumps(memory))
        else:
            raise RuntimeError("Unsupported backend or missing library")

    def get_solved_problems(self) -> List[str]:
        """Get list of categories marked as solved"""
        full_data = self.load()
        if "categories" not in full_data:
            return []
            
        solved = []
        for category, data in full_data["categories"].items():
            if data.get("solved", False):
                solved.append(category)
        return solved

    def mark_problem_solved(self, category: str, proof_data: Dict = None):
        """Mark a problem category as solved and optionally store the proof"""
        category_data = self.load(category)
        category_data["solved"] = True
        category_data["solved_timestamp"] = json.dumps({"timestamp": "now"})  # Simple timestamp
        
        if proof_data:
            if "formal_proofs" not in category_data:
                category_data["formal_proofs"] = []
            category_data["formal_proofs"].append(proof_data)
            
        self.save(category_data, category)

    def get_reusable_theorems(self, domain: str = None) -> List[Dict]:
        """Get proven theorems that could be reused in other problems"""
        full_data = self.load()
        if "categories" not in full_data:
            return []
            
        reusable_theorems = []
        for category, data in full_data["categories"].items():
            if data.get("solved", False):
                # Extract formal proofs and successful theorems
                for proof in data.get("formal_proofs", []):
                    if proof.get("success", False) and proof.get("verification_status") == "verified":
                        theorem_info = {
                            "source_category": category,
                            "theorem_name": proof.get("theorem_name", "unknown"),
                            "lean_statement": proof.get("lean_statement", ""),
                            "informal_statement": proof.get("informal_statement", ""),
                            "proof_attempt": proof.get("proof_attempt", ""),
                            "domain": data.get("domain", "unknown")
                        }
                        if not domain or theorem_info["domain"] == domain:
                            reusable_theorems.append(theorem_info)
                            
        return reusable_theorems
