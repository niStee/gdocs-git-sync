import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from gdocs_sync.parser import doc_to_markdown

class TestParser(unittest.TestCase):

    def test_parse_headings_and_paragraphs(self):
        doc_data = {
            "title": "Sample Document",
            "body": {
                "content": [
                    {
                        "paragraph": {
                            "paragraphStyle": {"namedStyleType": "HEADING_1"},
                            "elements": [{"textRun": {"content": "Heading One\n"}}]
                        }
                    },
                    {
                        "paragraph": {
                            "paragraphStyle": {"namedStyleType": "HEADING_2"},
                            "elements": [{"textRun": {"content": "Heading Two\n"}}]
                        }
                    },
                    {
                        "paragraph": {
                            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                            "elements": [
                                {"textRun": {"content": "This is a regular paragraph with "}},
                                {"textRun": {"content": "bold text", "textStyle": {"bold": True}}},
                                {"textRun": {"content": ".\n"}}
                            ]
                        }
                    }
                ]
            }
        }
        md = doc_to_markdown(doc_data)
        self.assertIn("# Heading One", md)
        self.assertIn("## Heading Two", md)
        self.assertIn("This is a regular paragraph with **bold text**.", md)

    def test_parse_bullet_lists(self):
        doc_data = {
            "title": "List Document",
            "body": {
                "content": [
                    {
                        "paragraph": {
                            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                            "bullet": {"listId": "kix.list.1"},
                            "elements": [{"textRun": {"content": "Item One\n"}}]
                        }
                    },
                    {
                        "paragraph": {
                            "paragraphStyle": {"namedStyleType": "NORMAL_TEXT"},
                            "bullet": {"listId": "kix.list.1"},
                            "elements": [{"textRun": {"content": "Item Two\n"}}]
                        }
                    }
                ]
            }
        }
        md = doc_to_markdown(doc_data)
        self.assertIn("- Item One", md)
        self.assertIn("- Item Two", md)

if __name__ == "__main__":
    unittest.main()
