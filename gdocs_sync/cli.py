import os
import sys
import argparse
from .config import load_config
from .client import GoogleDocsClient
from .sync import SyncManager

def main():
    parser = argparse.ArgumentParser(
        prog="gdocs-sync",
        description="Bi-directional synchronization between Google Docs and Git Markdown (Docs-as-Code)."
    )
    parser.add_argument(
        "-c", "--config",
        default="docs-sync.yaml",
        help="Path to docs-sync.yaml configuration file (default: docs-sync.yaml)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. status
    subparsers.add_parser("status", help="Check sync status and last modified timestamps of mapped documents")

    # 2. pull
    subparsers.add_parser("pull", help="Pull latest content from Google Docs and write to local Git Markdown files")

    # 3. diff
    subparsers.add_parser("diff", help="Show differences between local Git Markdown and remote Google Docs")

    args = parser.parse_args()

    if not os.path.isfile(args.config):
        print(f"❌ Error: Config file '{args.config}' not found.")
        print("💡 Create a docs-sync.yaml or specify one with -c /path/to/sync.yaml")
        sys.exit(1)

    try:
        cfg = load_config(args.config)
        client = GoogleDocsClient()
        base_dir = os.path.dirname(os.path.abspath(args.config))
        mgr = SyncManager(cfg, client, base_dir=base_dir)

        if args.command == "status":
            print(f"=== GDOCS-GIT-SYNC STATUS ({len(cfg.documents)} documents) ===\n")
            statuses = mgr.status()
            for s in statuses:
                doc = s["doc"]
                exists_str = "✅ Local Exists" if s["local_exists"] else "❌ Local Missing"
                r_meta = s["remote_meta"]
                mod_time = r_meta.get("modifiedTime", "Unknown") if "error" not in r_meta else f"Error: {r_meta['error']}"
                print(f"📄 {doc.title}")
                print(f"   Local:  {doc.file} ({exists_str})")
                print(f"   Remote: {doc.url}")
                print(f"   Modified: {mod_time}\n")

        elif args.command == "diff":
            diffs = mgr.diff()
            if not diffs:
                print("✅ Everything is up to date! Zero differences between local Git and Google Docs.")
            else:
                print(f"⚠️ Found differences in {len(diffs)} document(s):\n")
                for fpath, dtext in diffs.items():
                    print(f"--- Diff for {fpath} ---")
                    print(dtext)

        elif args.command == "pull":
            print(f"📥 Pulling {len(cfg.documents)} document(s) from Google Docs...")
            results = mgr.pull(write=True)
            for doc, _, changed in results:
                status_str = "UPDATED" if changed else "UNCHANGED"
                print(f"[{status_str:9}] {doc.title} -> {doc.file}")
            print("\n✅ Pull completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
