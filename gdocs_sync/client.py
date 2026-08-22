import json
import os
from typing import Any

import requests


class GoogleDocsClient:
    def __init__(self, token_path: str | None = None, creds_path: str | None = None):
        self.token_path = token_path or os.path.expanduser("~/.google-mcp/tokens/personal.json")
        self.creds_path = creds_path or os.path.expanduser("~/.google-mcp/credentials.json")
        self._access_token: str | None = None

    def get_access_token(self) -> str:
        if self._access_token:
            return self._access_token

        # 1. Try env var
        env_token = os.environ.get("GOOGLE_ACCESS_TOKEN")
        if env_token:
            self._access_token = env_token
            return env_token

        # 2. Refresh via ~/.google-mcp
        if not os.path.isfile(self.creds_path) or not os.path.isfile(self.token_path):
            raise RuntimeError(
                f"Google credentials not found at {self.creds_path} or {self.token_path}"
            )

        with open(self.creds_path) as f:
            cred_data = json.load(f)
            client_info = cred_data.get("installed") or cred_data.get("web") or cred_data

        client_id = client_info.get("client_id")
        client_secret = client_info.get("client_secret")

        with open(self.token_path) as f:
            token_data = json.load(f)

        refresh_token = token_data.get("refresh_token")

        resp = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        )

        if resp.status_code != 200:
            raise RuntimeError(f"OAuth token refresh failed: {resp.status_code} {resp.text}")

        self._access_token = resp.json().get("access_token")
        return self._access_token

    def get_document(self, doc_id: str) -> dict[str, Any]:
        token = self.get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://docs.googleapis.com/v1/documents/{doc_id}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to fetch document {doc_id}: {resp.status_code} {resp.text}")
        return resp.json()

    def get_drive_metadata(self, file_id: str) -> dict[str, Any]:
        token = self.get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=id,name,modifiedTime,version,webViewLink"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to fetch file metadata {file_id}: {resp.status_code}")
        return resp.json()
