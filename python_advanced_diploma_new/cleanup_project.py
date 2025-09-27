
"""
Cкрипт очистки пректа от мусорных файлов
"""

import os
import shutil
from pathlib import Path


def cleanup_project():
    # Текущая папка (где запущен скрипт)
    current_dir = Path.cwd()
    print(f"📁 Текущая папка: {current_dir}")

    # Файлы для удаления (относительные пути)
    files_to_remove = [
        "app/api/endpoints/models.py",
        "app/api/core/models.py",
        "app/auth/dependencies.py",
        "app/chat/utils.py",
    ]

    # Папки для очистки
    folders_to_remove = [
        "frontend/src/types",
    ]

    print("🔍 Поиск файлов для удаления...")

    # Проверяем файлы
    found_files = []
    for file_path in files_to_remove:
        full_path = current_dir / file_path
        if full_path.exists():
            found_files.append(full_path)
            print(f"✅ Найден: {file_path}")
        else:
            print(f"❌ Не найден: {file_path}")

    # Проверяем папки
    found_folders = []
    for folder_path in folders_to_remove:
        full_path = current_dir / folder_path
        if full_path.exists():
            found_folders.append(full_path)
            print(f"✅ Найдена папка: {folder_path}")
        else:
            print(f"❌ Не найдена папка: {folder_path}")

    if not found_files and not found_folders:
        print("🎉 Нечего удалять - проект уже чист!")
        return

    # Предпросмотр
    print(f"\n📋 Будет удалено:")
    for f in found_files:
        print(f"📄 {f.relative_to(current_dir)}")
    for f in found_folders:
        print(f"📁 {f.relative_to(current_dir)}")

    # Подтверждение
    confirm = input("\n⚠️ Удалить эти файлы? (y/N): ")
    if confirm.lower() == 'y':
        # Удаляем файлы
        for file_path in found_files:
            try:
                os.remove(file_path)
                print(f"✅ Удален: {file_path.relative_to(current_dir)}")
            except Exception as e:
                print(f"❌ Ошибка удаления {file_path}: {e}")

        # Удаляем папки
        for folder_path in found_folders:
            try:
                shutil.rmtree(folder_path)
                print(
                    f"✅ Удалена папка: {folder_path.relative_to(current_dir)}")
            except Exception as e:
                print(f"❌ Ошибка удаления папки {folder_path}: {e}")

        print("🎉 Очистка завершена!")
    else:
        print("❌ Очистка отменена")


if __name__ == "__main__":
    cleanup_project()