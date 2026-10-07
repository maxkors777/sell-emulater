#!/bin/bash
# Тест 3: ошибочные ситуации (окна со скриптами, остановленными на ошибке, закрывайте вручную)
cd "$(dirname "$0")/.." || exit 1
PY=python; command -v python >/dev/null 2>&1 || PY=python3

echo "== скрипт с неизвестной командой (остановка на foo) =="
$PY emulater.py --vfs vfs_root --script scripts/start_error.txt
echo "код выхода: $?"

echo "== скрипт с неверными аргументами (остановка на cd a b) =="
$PY emulater.py --vfs vfs_root --script scripts/start_bad_args.txt
echo "код выхода: $?"

echo "== несуществующий скрипт =="
$PY emulater.py --script scripts/no_such_file.txt
echo "код выхода: $?"

echo "== несуществующий VFS (ожидаем код 2) =="
$PY emulater.py --vfs /no/such/vfs
echo "код выхода: $?"

echo "== неизвестный параметр (ожидаем код 2) =="
$PY emulater.py --bogus
echo "код выхода: $?"

echo "== параметр без значения (ожидаем код 2) =="
$PY emulater.py --vfs
echo "код выхода: $?"
