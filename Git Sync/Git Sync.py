"""
Obsidian Vault Sync to GitHub
Author: Balasubramanian PG
Description: Syncs Obsidian vault files to GitHub with incremental updates
"""

import os
import sys
import json
import time
import shutil
import hashlib
import logging
import subprocess
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from enum import Enum

from git import Repo

# ============================================================================
# Configuration
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent  # 🔑 SCRIPT DIRECTORY

@dataclass
class Config:
    VAULT_PATH: Path = Path(r"C:\Users\ASUS\Videos\AnyDesk\Balasubramanian PG")
    GITHUB_REPO_URL: str = "https://github.com/Balasubramanian-pg/Obsidian.git"
    BRANCH: str = "main"

    PERSONAL_VAULT_FOLDER: str = "Personal Vault"

    BASE_PATH: Path = BASE_DIR
    CLONE_PATH: Path = BASE_DIR / "repo"
    STATE_PATH: Path = BASE_DIR / "state"

    GITHUB_TOKEN: Optional[str] = None

    MAX_FILE_SIZE_MB: int = 100

    INCLUDE_EXTENSIONS: List[str] = field(default_factory=lambda: [
        ".md", ".txt", ".png", ".jpg", ".jpeg", ".gif",
        ".pdf", ".svg", ".json", ".yaml", ".yml", ".csv"
    ])

    EXCLUDE_DIRS: List[str] = field(default_factory=lambda: [
        ".git", ".obsidian", "node_modules", "__pycache__"
    ])

    LOG_FILE: Path = BASE_DIR / "sync.log"


# ============================================================================
# Sync State
# ============================================================================

class SyncState:
    def __init__(self, path: Path):
        self.file = path / "sync_state.json"
        self.state: Dict[str, Dict] = {}
        self.load()

    def load(self):
        if self.file.exists():
            self.state = json.loads(self.file.read_text())
        else:
            self.state = {}

    def save(self):
        self.file.parent.mkdir(parents=True, exist_ok=True)
        self.file.write_text(json.dumps(self.state, indent=2))

    def update(self, rel_path: str, checksum: str):
        self.state[rel_path] = {
            "checksum": checksum,
            "timestamp": time.time()
        }

    def remove(self, rel_path: str):
        self.state.pop(rel_path, None)


# ============================================================================
# Logging
# ============================================================================

def setup_logging(config: Config):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ],
    )


# ============================================================================
# Utilities
# ============================================================================

def load_local_token(config: Config):
    env_file = config.BASE_PATH / ".env"

    if not env_file.exists():
        raise RuntimeError(f".env not found at {env_file}")

    for line in env_file.read_text().splitlines():
        if line.startswith("GITHUB_TOKEN="):
            config.GITHUB_TOKEN = line.split("=", 1)[1].strip()
            return

    raise RuntimeError("GITHUB_TOKEN not found in .env")


def checksum(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def should_include(path: Path, config: Config) -> bool:
    if path.stat().st_size > config.MAX_FILE_SIZE_MB * 1024 * 1024:
        return False
    if path.suffix.lower() not in config.INCLUDE_EXTENSIONS:
        return False
    if any(part in config.EXCLUDE_DIRS for part in path.parts):
        return False
    return True


# ============================================================================
# Git Manager
# ============================================================================

class GitManager:
    def __init__(self, config: Config):
        self.config = config
        self.repo: Optional[Repo] = None
        self.target_root = config.CLONE_PATH / config.PERSONAL_VAULT_FOLDER

    def setup_auth(self):
        subprocess.run(
            ["git", "config", "--global", "credential.helper", "store"],
            check=True
        )

        subprocess.run(
            ["git", "credential", "approve"],
            input=f"""protocol=https
host=github.com
username={self.config.GITHUB_TOKEN}
password=x-oauth-basic

""",
            text=True,
            check=True
        )

    def clone_or_pull(self):
        self.setup_auth()

        if self.config.CLONE_PATH.exists():
            self.repo = Repo(self.config.CLONE_PATH)
            self.repo.git.fetch()
            self.repo.git.checkout(self.config.BRANCH)
            self.repo.git.pull()
        else:
            self.repo = Repo.clone_from(
                self.config.GITHUB_REPO_URL,
                self.config.CLONE_PATH,
                branch=self.config.BRANCH
            )

        self.target_root.mkdir(parents=True, exist_ok=True)

    def commit_and_push(self, message: str):
        self.repo.git.add(all=True)

        if not self.repo.is_dirty():
            logging.info("No changes to commit")
            return

        self.repo.index.commit(message)
        self.repo.remotes.origin.push()


# ============================================================================
# Sync Engine
# ============================================================================

class ObsidianSyncEngine:
    def __init__(self, config: Config):
        self.config = config
        self.state = SyncState(config.STATE_PATH)
        self.git = GitManager(config)

    def run(self):
        setup_logging(self.config)
        load_local_token(self.config)

        if not self.config.VAULT_PATH.exists():
            raise RuntimeError("Vault path does not exist")

        self.git.clone_or_pull()

        seen = set()
        updated = 0
        deleted = 0

        for file in self.config.VAULT_PATH.rglob("*"):
            if not file.is_file() or not should_include(file, self.config):
                continue

            rel = str(file.relative_to(self.config.VAULT_PATH))
            seen.add(rel)

            cs = checksum(file)
            old = self.state.state.get(rel)

            if old and old["checksum"] == cs:
                continue

            target = self.git.target_root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, target)

            self.state.update(rel, cs)
            updated += 1

        for rel in list(self.state.state.keys()):
            if rel not in seen:
                target = self.git.target_root / rel
                if target.exists():
                    target.unlink()
                self.state.remove(rel)
                deleted += 1

        self.state.save()

        if updated or deleted:
            msg = f"Vault Sync: {updated} updated, {deleted} deleted ({datetime.now():%Y-%m-%d %H:%M:%S})"
            self.git.commit_and_push(msg)

        logging.info("Sync completed successfully")
        logging.info(f"Updated: {updated}, Deleted: {deleted}")


# ============================================================================
# Entry Point
# ============================================================================

def main():
    try:
        engine = ObsidianSyncEngine(Config())
        engine.run()
        return 0
    except Exception as e:
        logging.error(str(e))
        logging.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
