import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import tempfile
import unittest

from gdocs_sync.config import ConfigError, load_config


class TestConfig(unittest.TestCase):
    def test_valid_config_loading(self):
        yaml_content = """
documents:
  - file: "docs/policy.md"
    doc_id: "1HkhevBBy-TXIHW9qER6O-MAjqvveQygmYKnAoSsUHKs"
    title: "Volt FOSS Sustainability Policy"
"""
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            config_path = f.name

        try:
            cfg = load_config(config_path)
            self.assertEqual(len(cfg.documents), 1)
            doc = cfg.documents[0]
            self.assertEqual(doc.file, "docs/policy.md")
            self.assertEqual(doc.doc_id, "1HkhevBBy-TXIHW9qER6O-MAjqvveQygmYKnAoSsUHKs")
            self.assertEqual(doc.title, "Volt FOSS Sustainability Policy")
            self.assertEqual(
                doc.url,
                "https://docs.google.com/document/d/1HkhevBBy-TXIHW9qER6O-MAjqvveQygmYKnAoSsUHKs/edit",
            )
        finally:
            os.remove(config_path)

    def test_missing_field_raises_error(self):
        yaml_content = """
documents:
  - file: "docs/policy.md"
"""
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            config_path = f.name

        try:
            with self.assertRaises(ConfigError):
                load_config(config_path)
        finally:
            os.remove(config_path)


if __name__ == "__main__":
    unittest.main()
