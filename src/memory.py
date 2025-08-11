import os
import json
from typing import Optional

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
    def __init__(self, config: Optional[dict] = None):
        self.backend = config.get("backend", MemoryBackend.FILE) if config else MemoryBackend.FILE
        # Set memory.json path relative to the project root directory
        self.file_path = self._get_memory_path()
        self.mongo_uri = config.get("mongo_uri") if config else None
        self.mongo_db = config.get("mongo_db", "pocketresearcher") if config else "pocketresearcher"
        self.mongo_collection = config.get("mongo_collection", "memory") if config else "memory"
        self.memcached_host = config.get("memcached_host", "127.0.0.1:11211") if config else "127.0.0.1:11211"
        self._setup_backend()

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

    def load(self):
        if self.backend == MemoryBackend.FILE:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    return json.load(f)
            return {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": []}
        elif self.backend == MemoryBackend.MONGODB and pymongo:
            doc = self.collection.find_one({"_id": "memory"})
            if doc:
                return doc.get("data", {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": []})
            return {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": []}
        elif self.backend == MemoryBackend.MEMCACHED and memcache:
            data = self.mc.get("memory")
            if data:
                return json.loads(data)
            return {"facts": [], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": []}
        else:
            raise RuntimeError("Unsupported backend or missing library")

    def save(self, memory):
        if self.backend == MemoryBackend.FILE:
            with open(self.file_path, "w") as f:
                json.dump(memory, f, indent=2)
        elif self.backend == MemoryBackend.MONGODB and pymongo:
            self.collection.update_one({"_id": "memory"}, {"$set": {"data": memory}}, upsert=True)
        elif self.backend == MemoryBackend.MEMCACHED and memcache:
            self.mc.set("memory", json.dumps(memory))
        else:
            raise RuntimeError("Unsupported backend or missing library")
