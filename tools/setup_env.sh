#!/usr/bin/env bash
# patent-drafting 专用 conda 环境一键搭建/修复（幂等：已存在则跳过对应步骤）。
# 用法： bash <SKILL_DIR>/tools/setup_env.sh   （SKILL_DIR=本技能安装根目录；脚本自身以 $0 定位，无需手设）
# 注意：所有 conda run 均带 --no-capture-output——否则 Windows 下 conda 用 GBK 重编码子进程输出会崩，
#       且 capture 模式不透传 stdin（会让 heredoc/交互脚本静默失效）。
set -e
ENV=patent-drafting
HERE="$(cd "$(dirname "$0")" && pwd)"          # tools/
RUN="conda run --no-capture-output -n $ENV"

echo "[1/5] conda 环境"
if conda env list | grep -qiE "[/\\\\]envs[/\\\\]${ENV}\$|^${ENV}[[:space:]]"; then
  echo "      $ENV 已存在，跳过创建"
else
  echo "      创建 $ENV (python 3.11)"
  conda create -n "$ENV" python=3.11 -y
fi

echo "[2/5] Python 包 (playwright/mammoth/python-pptx/python-docx/matplotlib)"
$RUN python -m pip install -r "$HERE/requirements.txt" -r "$HERE/requirements-cnipa.txt"

echo "[3/5] playwright chromium 浏览器"
$RUN python -m playwright install chromium

echo "[4/5] nodejs + mermaid-cli (交底书流程图渲染)"
$RUN node --version >/dev/null 2>&1 || conda install -n "$ENV" -c conda-forge nodejs -y
$RUN mmdc --version >/dev/null 2>&1 || $RUN npm install -g @mermaid-js/mermaid-cli

echo "[5/5] 生成 puppeteer 配置（指向本机 playwright chromium；机器本地、不入库）"
$RUN python "$HERE/gen_puppeteer_config.py" "$HERE/puppeteer-config.json"

echo "[done] patent-drafting 环境就绪。所有工具用： conda run --no-capture-output -n patent-drafting python <tool>"
