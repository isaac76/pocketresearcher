import unittest
from unittest.mock import patch, MagicMock, mock_open
from src.memory import Memory, MemoryBackend

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.sample_memory = {"facts": ["A fact"], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": []}

    @patch("builtins.open", new_callable=mock_open, read_data='{"facts": ["A fact"], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": []}')
    @patch("os.path.exists", return_value=True)
    def test_file_backend_load_and_save(self, mock_exists, mock_file):
        mem = Memory(category="test_category", config={"backend": MemoryBackend.FILE, "file_path": "test_memory.json"})
        loaded = mem.load(category="test_category")
        self.assertEqual(loaded["facts"], ["A fact"])
        mem.save(self.sample_memory, category="test_category")
        mock_file().write.assert_called()

    @patch("src.memory.pymongo")
    def test_mongodb_backend_load_and_save(self, mock_pymongo):
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {"_id": "memory", "data": self.sample_memory}
        mock_client = MagicMock()
        mock_client.__getitem__.return_value = {"memory": mock_collection}
        mock_pymongo.MongoClient.return_value = mock_client
        mem = Memory(category="test_category", config={"backend": MemoryBackend.MONGODB, "mongo_uri": "mongodb://localhost", "mongo_db": "testdb", "mongo_collection": "memory"})
        loaded = mem.load(category="test_category")
        self.assertEqual(loaded["facts"], ["A fact"])
        mem.save(self.sample_memory, category="test_category")
        mock_collection.update_one.assert_called()

    @patch("src.memory.memcache")
    def test_memcached_backend_load_and_save(self, mock_memcache):
        mock_mc = MagicMock()
        mock_mc.get.return_value = '{"facts": ["A fact"], "ideas": [], "reflections": [], "proofs": [], "techniques": [], "experiments": []}'
        mock_memcache.Client.return_value = mock_mc
        mem = Memory(category="test_category", config={"backend": MemoryBackend.MEMCACHED, "memcached_host": "127.0.0.1:11211"})
        loaded = mem.load(category="test_category")
        self.assertEqual(loaded["facts"], ["A fact"])
        mem.save(self.sample_memory, category="test_category")
        mock_mc.set.assert_called()

if __name__ == "__main__":
    unittest.main()
