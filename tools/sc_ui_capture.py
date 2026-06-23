#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sc_ui_capture.py — 软著操作说明书界面截图（Tier 2，仅 Web/Electron 较可行，可选）。

用 playwright(chromium) 打开本地运行的 Web 前端，按给定路由依次截图，回填说明书的"图X"占位。
本工具是**最佳努力**：playwright 缺失、服务未起、路由打不开等任何失败都**显式报告并非零退出**，
由 Agent 据此降级到 Tier 1（读码生文+占位）/ Tier 3（引导用户补图）。桌面栈(Qt/Tk/MATLAB)不在本工具范围。

用法：
  # 先在另一终端把前端跑起来（如 npm run dev，监听 http://localhost:3000）
  python sc_ui_capture.py --url http://localhost:3000 --out ./截图 \
      --route /:主界面 --route /import:导入界面 --route /result:结果界面

每个 --route 形如 `路径:中文图题`；不带冒号则图题取路径。截图命名 图1_主界面.png ...
依赖：playwright（已在 conda 环境 patent-drafting 中；首次需 python -m playwright install chromium）。
"""
import argparse
import os
import sys
import time


def parse_routes(route_args):
    routes = []
    for r in route_args or []:
        if ":" in r:
            path, title = r.split(":", 1)
        else:
            path, title = r, r
        routes.append((path.strip() or "/", title.strip() or path.strip() or "page"))
    if not routes:
        routes = [("/", "主界面")]
    return routes


def main():
    ap = argparse.ArgumentParser(description="软著说明书界面截图（Web/Electron，Tier 2）")
    ap.add_argument("--url", required=True, help="前端基地址，如 http://localhost:3000")
    ap.add_argument("--out", default="截图", help="截图输出目录")
    ap.add_argument("--route", action="append", default=[], help="`路径:图题`，可多次；默认 /:主界面")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=1024)
    ap.add_argument("--wait", type=float, default=1.5, help="每页加载后等待秒数")
    ap.add_argument("--full-page", action="store_true", help="整页截图（默认仅视口）")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[降级] 未安装 playwright，无法自动截图。请改用 Tier 1（占位）+ Tier 3（引导用户补图）。\n"
              "       如需启用：在 conda 环境 patent-drafting 中 python -m playwright install chromium。",
              file=sys.stderr)
        sys.exit(3)

    routes = parse_routes(args.route)
    os.makedirs(args.out, exist_ok=True)
    base = args.url.rstrip("/")
    ok, fail = 0, 0
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": args.width, "height": args.height})
            for i, (path, title) in enumerate(routes, 1):
                target = base + ("" if path == "/" else "/" + path.lstrip("/"))
                fname = os.path.join(args.out, f"图{i}_{title}.png")
                try:
                    page.goto(target, wait_until="networkidle", timeout=15000)
                    time.sleep(args.wait)
                    page.screenshot(path=fname, full_page=args.full_page)
                    print(f"[OK] 图{i} {title} <- {target} -> {fname}")
                    ok += 1
                except Exception as e:  # noqa: BLE001 单页失败不致命
                    print(f"[失败] 图{i} {title} <- {target}: {e}", file=sys.stderr)
                    fail += 1
            browser.close()
    except Exception as e:  # noqa: BLE001 浏览器/服务整体不可用
        print(f"[降级] 浏览器或前端服务不可用：{e}\n       请确认前端已在 {args.url} 运行；否则改用 Tier 1/Tier 3。",
              file=sys.stderr)
        sys.exit(3)

    print(f"==== 截图完成：成功 {ok}，失败 {fail} ====")
    if fail:
        print("部分界面未截到：对缺图项改用 Tier 3（在说明书中保留占位，并给用户截图清单）。", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
