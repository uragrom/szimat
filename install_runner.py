# -*- coding: utf-8 -*-
"""
Launcher for context menu installation. Shows Russian messages and checks admin.
Run from install.bat (batch file must be ASCII-only to avoid encoding issues).
"""
import sys
import ctypes
import os
from pathlib import Path


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def main():
    if not is_admin():
        print("=" * 50)
        print("ОШИБКА: Требуются права администратора!")
        print("Запустите install.bat от имени администратора:")
        print("  ПКМ по install.bat -> Запуск от имени администратора")
        print("=" * 50)
        sys.exit(1)

    os.chdir(Path(__file__).resolve().parent)
    print("========================================")
    print("Установка пунктов «Сжать» и «Конвертация» в контекстное меню")
    print("========================================")
    print()

    try:
        import install_context_menu
        if len(sys.argv) > 1 and sys.argv[1] == '--remove':
            print("Удаление пунктов из контекстного меню...")
            print()
            install_context_menu.remove_from_registry()
            print()
            print("Удаление завершено. Перезапустите проводник при необходимости.")
        else:
            install_context_menu.add_to_registry()
            print()
            print("========================================")
            print("Установка завершена успешно!")
            print("========================================")
            print()
            print("Чтобы изменения вступили в силу:")
            print("  1. Перезапустите проводник (Ctrl+Shift+Esc -> Найти explorer.exe -> Перезапустить)")
            print("  2. Или перезагрузите компьютер")
            print()
    except SystemExit as e:
        if e.code != 0:
            print()
            print("========================================")
            print("Ошибка при установке!")
            print("========================================")
        raise
    except Exception as e:
        print()
        print("========================================")
        print("Ошибка при установке:", e)
        print("========================================")
        sys.exit(1)


if __name__ == '__main__':
    main()
