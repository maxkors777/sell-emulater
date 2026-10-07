#!/bin/bash
# Тест 2: параметры --vfs и --script
cd "$(dirname "$0")/.." || exit 1
PY=python; command -v python >/dev/null 2>&1 || PY=python3

echo "== --vfs + --script (скрипт без ошибок, завершается командой exit) =="
$PY emulater.py --vfs vfs_root --script scripts/start_ok.txt
echo "код выхода: $?"

echo "== только --vfs (закройте окно) =="
$PY emulater.py --vfs vfs_root
echo "код выхода: $?"

echo "== только --script (закройте окно после выполнения) =="
$PY emulater.py --script scripts/start_ok.txt
echo "код выхода: $?"
