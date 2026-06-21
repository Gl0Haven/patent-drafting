#!/usr/bin/env python
"""生成 puppeteer-config.json（供 mermaid_render.py 以 -p 传入），指向本机 playwright chromium。

用法：
    python gen_puppeteer_config.py [输出路径]
不传输出路径时，默认写到本脚本同目录的 puppeteer-config.json。
该文件含本机 chromium 绝对路径，机器本地、已 .gitignore，不入库。
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "puppeteer-config.json"
with sync_playwright() as p:
    exe = p.chromium.executable_path
out.write_text(
    json.dumps({"executablePath": exe, "args": ["--no-sandbox"]}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print("puppeteer-config.json ->", exe)
