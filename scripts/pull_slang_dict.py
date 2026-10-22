#!/usr/bin/env python3
"""从 jshdcn/underground-slang-lexicon 拉取合并后的词典产物。

数据流：上游 threathunterX/underground-slang-lexicon →（本仓库 fork 定时合并）
       → skill/*.md → 本技能的 references/

用法：
  python3 scripts/pull_slang_dict.py            # 有更新才写盘
  python3 scripts/pull_slang_dict.py --force    # 强制重写
  python3 scripts/pull_slang_dict.py --check    # 只检查，有更新则退出码 2

零第三方依赖。
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path

FORK = "jshdcn/underground-slang-lexicon"
REF = "main"
API = f"https://api.github.com/repos/{FORK}/commits/{REF}"
RAW = f"https://raw.githubusercontent.com/{FORK}"
ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "references"
FILES = ["underground-slang-lexicon.md", "underground-slang-index.md"]


def fetch(url: str) -> bytes:
    last: Exception | None = None
    for _ in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "anti-cheating-assistant-pull"},
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            last = exc
    raise RuntimeError(f"下载失败：{url}（{last}）")


def latest_commit() -> str:
    try:
        response = json.loads(fetch(API))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"GitHub API 返回了无法解析的 JSON：{API}") from exc
    if not isinstance(response, dict):
        raise RuntimeError(f"GitHub API 响应格式异常：{API}")
    sha = response.get("sha")
    if not isinstance(sha, str) or not sha:
        raise RuntimeError(f"无法从 GitHub API 响应中取得 {FORK}/{REF} 的 commit SHA")
    return sha


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="拉取合并后的黑话词典")
    ap.add_argument("--force", action="store_true", help="忽略内容比较，强制重写")
    ap.add_argument("--check", action="store_true", help="仅检查是否有更新")
    args = ap.parse_args(argv)

    try:
        sha = latest_commit()
    except RuntimeError as exc:
        print(f"{exc}\n（请确认 fork 的 main 已完成首次构建并提交词典文件）", file=sys.stderr)
        return 1

    try:
        downloaded = {
            name: fetch(f"{RAW}/{sha}/skill/{name}")
            for name in FILES
        }
    except RuntimeError as exc:
        print(f"{exc}\n（请确认 {sha[:10]} 中包含已构建的 skill 词典文件）", file=sys.stderr)
        return 1

    stale = [
        name for name, data in downloaded.items()
        if args.force or not (DEST / name).exists() or (DEST / name).read_bytes() != data
    ]

    if not stale:
        print(f"已是最新（词典仓库 commit {sha[:10]}）")
        return 0
    if args.check:
        print(f"有更新：{', '.join(stale)}（词典仓库 commit {sha[:10]}）")
        return 2

    DEST.mkdir(parents=True, exist_ok=True)
    for name in stale:
        data = downloaded[name]
        (DEST / name).write_bytes(data)
        print(f"  更新 {name}（{len(data) // 1024}KB）")

    print(f"完成：词典仓库 commit {sha[:10]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
