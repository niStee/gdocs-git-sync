import os
import yaml
from dataclasses import dataclass
from typing import List, Optional

class ConfigError(Exception):
    pass

@dataclass
class DocumentMapping:
    file: str
    doc_id: str
    title: Optional[str] = None
    url: Optional[str] = None

    def __post_init__(self):
        if not self.url and self.doc_id:
            self.url = f"https://docs.google.com/document/d/{self.doc_id}/edit"
        if not self.title:
            self.title = os.path.basename(self.file)

@dataclass
class SyncConfig:
    documents: List[DocumentMapping]

def load_config(config_path: str) -> SyncConfig:
    if not os.path.isfile(config_path):
        raise ConfigError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f) or {}
        except Exception as e:
            raise ConfigError(f"YAML parsing error: {e}")

    raw_docs = data.get("documents", [])
    if not isinstance(raw_docs, list):
        raise ConfigError("'documents' must be a list in config file")

    mappings = []
    for idx, item in enumerate(raw_docs):
        if not isinstance(item, dict):
            raise ConfigError(f"Document entry #{idx} must be a dictionary")
        if "file" not in item:
            raise ConfigError(f"Document entry #{idx} missing required 'file' key")
        if "doc_id" not in item:
            raise ConfigError(f"Document entry #{idx} missing required 'doc_id' key")

        mappings.append(DocumentMapping(
            file=item["file"],
            doc_id=item["doc_id"],
            title=item.get("title"),
            url=item.get("url")
        ))

    return SyncConfig(documents=mappings)
