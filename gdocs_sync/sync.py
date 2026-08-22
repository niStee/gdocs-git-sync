import difflib
import os
from typing import Any

from .client import GoogleDocsClient
from .config import DocumentMapping, SyncConfig
from .parser import doc_to_markdown


class SyncManager:
    def __init__(self, config: SyncConfig, client: GoogleDocsClient, base_dir: str = "."):
        self.config = config
        self.client = client
        self.base_dir = os.path.abspath(base_dir)

    def resolve_path(self, rel_path: str) -> str:
        return os.path.join(self.base_dir, rel_path)

    def status(self) -> list[dict[str, Any]]:
        results = []
        for doc in self.config.documents:
            local_path = self.resolve_path(doc.file)
            local_exists = os.path.isfile(local_path)
            local_mtime = os.path.getmtime(local_path) if local_exists else None

            remote_meta = {}
            try:
                remote_meta = self.client.get_drive_metadata(doc.doc_id)
            except Exception as e:
                remote_meta = {"error": str(e)}

            results.append(
                {
                    "doc": doc,
                    "local_path": local_path,
                    "local_exists": local_exists,
                    "local_mtime": local_mtime,
                    "remote_meta": remote_meta,
                }
            )
        return results

    def pull(self, write: bool = True) -> list[tuple[DocumentMapping, str, bool]]:
        pulled = []
        for doc in self.config.documents:
            doc_data = self.client.get_document(doc.doc_id)
            md_content = doc_to_markdown(doc_data)

            local_path = self.resolve_path(doc.file)
            changed = True
            if os.path.isfile(local_path):
                with open(local_path, encoding="utf-8") as f:
                    existing = f.read()
                changed = existing != md_content

            if write and changed:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(md_content)

            pulled.append((doc, md_content, changed))
        return pulled

    def diff(self) -> dict[str, str]:
        diffs = {}
        for doc in self.config.documents:
            doc_data = self.client.get_document(doc.doc_id)
            remote_md = doc_to_markdown(doc_data)

            local_path = self.resolve_path(doc.file)
            local_content = ""
            if os.path.isfile(local_path):
                with open(local_path, encoding="utf-8") as f:
                    local_content = f.read()

            diff_lines = list(
                difflib.unified_diff(
                    local_content.splitlines(keepends=True),
                    remote_md.splitlines(keepends=True),
                    fromfile=f"a/{doc.file} (local Git)",
                    tofile=f"b/{doc.file} (Google Docs)",
                )
            )

            if diff_lines:
                diffs[doc.file] = "".join(diff_lines)
        return diffs
