#!/bin/bash
# Тест 1: запуск без параметров (закройте окно или введите exit)
cd "$(dirname "$0")/.." || exit 1
PY=python; command -v python >/dev/null 2>&1 || PY=python3

echo "== запуск без параметров =="
$PY emulater.py
echo "код выхода: $?"
