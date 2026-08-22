import os
import unittest
import tempfile
from unittest.mock import MagicMock
from gdocs_sync.config import SyncConfig, DocumentMapping
from gdocs_sync.sync import SyncManager

class TestSyncManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.doc_mapping = DocumentMapping(
            file="test_doc.md",
            doc_id="mock-123",
            title="Mock Document"
        )
        self.config = SyncConfig(documents=[self.doc_mapping])
        self.mock_client = MagicMock()

    def tearDown(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_pull_writes_file(self):
        mock_doc_data = {
            "title": "Mock Title",
            "body": {
                "content": [
                    {
                        "paragraph": {
                            "paragraphStyle": {"namedStyleType": "HEADING_1"},
                            "elements": [{"textRun": {"content": "Hello World\n"}}]
                        }
                    }
                ]
            }
        }
        self.mock_client.get_document.return_value = mock_doc_data

        mgr = SyncManager(self.config, self.mock_client, base_dir=self.temp_dir)
        results = mgr.pull(write=True)

        self.assertEqual(len(results), 1)
        doc, content, changed = results[0]
        self.assertTrue(changed)
        self.assertEqual(content.strip(), "# Hello World")

        written_file = os.path.join(self.temp_dir, "test_doc.md")
        self.assertTrue(os.path.isfile(written_file))
        with open(written_file, "r") as f:
            self.assertEqual(f.read().strip(), "# Hello World")

if __name__ == "__main__":
    unittest.main()
