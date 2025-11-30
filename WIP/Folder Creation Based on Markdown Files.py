import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Dict, Set

# default vault path (use a raw string literal)
DEFAULT_VAULT = Path(r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\SQL 101\SQL Reading Material")

ATTACH_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".csv", ".xlsx", ".xls", ".zip", ".mp3", ".ogg"}

_SAFE_NAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1F]')
_WHITESPACE_RE = re.compile(r'\s+')

MD_LINK_RE = re.compile(r'(!?)\[(?P<label>[^\]]*)\]\((?P<target>[^)\s]+)(?P<rest>[^)]*)\)')
WIKI_LINK_RE = re.compile(r'\[\[(?P<target>[^\]\|]+)(\|(?P<alias>[^\]]+))?\]\]')

def safe_folder_name(name: str) -> str:
    name = name.strip()
    name = _WHITESPACE_RE.sub(" ", name)
    name = _SAFE_NAME_RE.sub("", name)
    name = name.rstrip(". ")
    return name or "untitled"

def find_markdown_files(root: Path):
    return [p for p in root.rglob("*.md") if p.is_file()]

def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")

def write_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8")

def create_backup(vault: Path, dry_run: bool):
    backup_name = vault.parent / f"{vault.name}_backup.zip"
    if dry_run:
        print(f"[DRY RUN] Would create backup: {backup_name}")
        return backup_name
    print(f"Creating backup: {backup_name}")
    with zipfile.ZipFile(backup_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in vault.rglob("*"):
            arcname = file.relative_to(vault.parent)
            zf.write(file, arcname.as_posix())
    print("Backup created.")
    return backup_name

def build_moved_map(md_files: Set[Path], vault_root: Path) -> Dict[str, str]:
    moved_map = {}
    for md in md_files:
        rel_orig = md.relative_to(vault_root).as_posix()
        parent = md.parent
        folder_name = safe_folder_name(md.stem)
        candidate = parent / folder_name
        if md.parent.name == md.stem:
            moved_map[rel_orig] = rel_orig
            continue
        final_folder = candidate
        suffix = 0
        while final_folder.exists() and not final_folder.is_dir():
            suffix += 1
            final_folder = parent / f"{folder_name}_{suffix}"
        new_md = final_folder / md.name
        if new_md.exists():
            i = 1
            base = md.stem
            ext = md.suffix
            while (final_folder / f"{base}_{i}{ext}").exists():
                i += 1
            new_md = final_folder / f"{base}_{i}{ext}"
        moved_map[rel_orig] = new_md.relative_to(vault_root).as_posix()
    return moved_map

def move_markdowns(moved_map: Dict[str,str], vault_root: Path, dry_run: bool):
    for rel_orig, rel_new in moved_map.items():
        if rel_orig == rel_new:
            print(f"[SKIP] {rel_orig} (already organized)")
            continue
        orig = vault_root / rel_orig
        new = vault_root / rel_new
        target_folder = new.parent
        if dry_run:
            print(f"[DRY RUN] Would create folder: {target_folder.relative_to(vault_root).as_posix()}")
            print(f"[DRY RUN] Would move: {rel_orig} -> {rel_new}")
        else:
            target_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(orig), str(new))
            print(f"Moved: {rel_orig} -> {rel_new}")

def move_attachments_for_notes(vault_root: Path, dry_run: bool) -> Dict[str,str]:
    moved_attachments = {}
    all_md = [p for p in vault_root.rglob("*.md") if p.is_file()]
    for md in all_md:
        text = read_text(md)
        for m in MD_LINK_RE.finditer(text):
            is_image = m.group(1) == "!"
            target = m.group("target")
            if target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:"):
                continue
            target_path = Path(target.split("#")[0])
            ext = target_path.suffix.lower()
            if ext not in ATTACH_EXTENSIONS:
                continue
            abs_ref = (md.parent / target_path).resolve()
            try:
                rel_ref = abs_ref.relative_to(vault_root).as_posix()
            except Exception:
                continue
            src = vault_root / rel_ref
            if not src.exists():
                continue
            dest = md.parent / target_path.name
            if dest.exists():
                i = 1
                base = target_path.stem
                ext = target_path.suffix
                while (md.parent / f"{base}_{i}{ext}").exists():
                    i += 1
                dest = md.parent / f"{base}_{i}{ext}"
            if dry_run:
                print(f"[DRY RUN] Would move attachment: {rel_ref} -> {dest.relative_to(vault_root).as_posix()}")
            else:
                src.rename(dest)
                print(f"Moved attachment: {rel_ref} -> {dest.relative_to(vault_root).as_posix()}")
            moved_attachments[rel_ref] = dest.relative_to(vault_root).as_posix()
    return moved_attachments

def update_links_across_vault(vault_root: Path, moved_map: Dict[str,str], attachment_moves: Dict[str,str], dry_run: bool):
    unified = {}
    unified.update(moved_map)
    unified.update(attachment_moves)
    all_md = [p for p in vault_root.rglob("*.md") if p.is_file()]
    for md in all_md:
        text = read_text(md)
        base_dir = md.parent
        new_text = text
        def md_repl(m):
            prefix = m.group(1)
            label = m.group("label")
            target = m.group("target")
            rest = m.group("rest") or ""
            if target.startswith("http://") or target.startswith("https://") or target.startswith("mailto:"):
                return m.group(0)
            target_path = Path(target.split("#")[0])
            try:
                resolved = (base_dir / target_path).resolve()
                rel_to_vault = resolved.relative_to(vault_root).as_posix()
            except Exception:
                return m.group(0)
            if rel_to_vault in unified:
                new_rel = unified[rel_to_vault]
                new_abs = vault_root / new_rel
                try:
                    relpath = new_abs.relative_to(base_dir).as_posix()
                except Exception:
                    relpath = new_abs.as_posix()
                anchor = ""
                if "#" in target:
                    anchor = "#" + target.split("#",1)[1]
                return f"{prefix}[{label}]({relpath}{anchor}{rest})"
            return m.group(0)
        new_text = MD_LINK_RE.sub(md_repl, new_text)
        def wiki_repl(m):
            target = m.group("target")
            alias = m.group("alias") or ""
            target_path = Path(target.split("#")[0])
            try:
                resolved = (base_dir / target_path).resolve()
                rel_to_vault = resolved.relative_to(vault_root).as_posix()
            except Exception:
                return m.group(0)
            if rel_to_vault in unified:
                new_rel = unified[rel_to_vault]
                new_abs = vault_root / new_rel
                try:
                    relpath = new_abs.relative_to(base_dir).as_posix()
                except Exception:
                    relpath = new_abs.as_posix()
                anchor = ""
                if "#" in target:
                    anchor = "#" + target.split("#",1)[1]
                if alias:
                    return f"[[{relpath}{anchor}|{alias}]]"
                return f"[[{relpath}{anchor}]]"
            return m.group(0)
        new_text = WIKI_LINK_RE.sub(wiki_repl, new_text)
        if new_text != text:
            if dry_run:
                print(f"[DRY RUN] Would update links in {md.relative_to(vault_root).as_posix()}")
            else:
                write_text(md, new_text)
                print(f"Updated links in {md.relative_to(vault_root).as_posix()}")

def main():
    parser = argparse.ArgumentParser(description="Organize vault: one folder per markdown file.")
    parser.add_argument("--vault", type=Path, default=DEFAULT_VAULT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--move-attachments", action="store_true")
    parser.add_argument("--update-links", action="store_true")
    parser.add_argument("--backup", action="store_true")
    args = parser.parse_args()

    vault_root = args.vault.expanduser().resolve()
    if not vault_root.exists() or not vault_root.is_dir():
        print("Vault not found:", vault_root)
        sys.exit(1)

    if args.backup:
        create_backup(vault_root, dry_run=args.dry_run)

    md_list = find_markdown_files(vault_root)
    print(f"Found {len(md_list)} markdown files.")

    moved_map = build_moved_map(set(md_list), vault_root)
    move_markdowns(moved_map, vault_root, dry_run=args.dry_run)

    attachment_moves = {}
    if args.move_attachments:
        attachment_moves = move_attachments_for_notes(vault_root, dry_run=args.dry_run)

    if args.update_links:
        update_links_across_vault(vault_root, moved_map, attachment_moves, dry_run=args.dry_run)

    print("Done.")

if __name__ == "__main__":
    main()