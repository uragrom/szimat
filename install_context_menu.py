#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для добавления пунктов "Сжать" и "Конвертировать" в контекстное меню Windows
для видео файлов
"""

import os
import sys
import winreg
from pathlib import Path


def get_script_path(script_name='compress_video.py'):
    """Получает абсолютный путь к скрипту"""
    # Путь к текущему скрипту
    current_dir = Path(__file__).parent.absolute()
    script_path = current_dir / script_name
    
    # Получаем путь к Python
    python_exe = sys.executable
    
    # Формируем команду для запуска
    return f'"{python_exe}" "{script_path}" "%1"'


def add_to_registry():
    """Добавляет записи в реестр Windows"""
    # Расширения файлов
    video_extensions = [
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', 
        '.flv', '.webm', '.m4v', '.3gp', '.mpg', '.mpeg'
    ]
    
    audio_extensions = [
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.ac3'
    ]
    
    image_extensions = [
        '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.webp', '.heic', '.heif'
    ]
    
    # Команды для запуска
    compress_command = get_script_path('compress_video.py')
    convert_command = get_script_path('convert_video.py')
    
    try:
        # Добавляем "Сжать" для всех файлов (фото, видео, аудио)
        base_key = r'*\shell'
        key = winreg.OpenKey(
            winreg.HKEY_CLASSES_ROOT,
            base_key,
            0,
            winreg.KEY_WRITE
        )
        
        try:
            compress_key = winreg.CreateKey(key, 'Сжать')
        except FileExistsError:
            compress_key = winreg.OpenKey(key, 'Сжать', 0, winreg.KEY_WRITE)
        
        try:
            command_key = winreg.CreateKey(compress_key, 'command')
        except FileExistsError:
            command_key = winreg.OpenKey(compress_key, 'command', 0, winreg.KEY_WRITE)
        
        winreg.SetValueEx(command_key, '', 0, winreg.REG_SZ, compress_command)
        winreg.CloseKey(command_key)
        winreg.CloseKey(compress_key)
        winreg.CloseKey(key)
        
        print("✓ Пункт 'Сжать' добавлен для всех файлов")
        
        # Добавляем "Конвертация" для всех файлов (фото, видео, аудио)
        base_key = r'*\shell'
        key = winreg.OpenKey(
            winreg.HKEY_CLASSES_ROOT,
            base_key,
            0,
            winreg.KEY_WRITE
        )
        
        try:
            convert_key = winreg.CreateKey(key, 'Конвертация')
        except FileExistsError:
            convert_key = winreg.OpenKey(key, 'Конвертация', 0, winreg.KEY_WRITE)
        
        try:
            command_key = winreg.CreateKey(convert_key, 'command')
        except FileExistsError:
            command_key = winreg.OpenKey(convert_key, 'command', 0, winreg.KEY_WRITE)
        
        winreg.SetValueEx(command_key, '', 0, winreg.REG_SZ, convert_command)
        winreg.CloseKey(command_key)
        winreg.CloseKey(convert_key)
        winreg.CloseKey(key)
        
        print("✓ Пункт 'Конвертация' добавлен для всех файлов")
        
        # Добавляем "Сжать" и "Конвертация" для видео расширений
        for ext in video_extensions:
            try:
                ext_key_path = f'{ext}\\shell'
                ext_key = winreg.OpenKey(
                    winreg.HKEY_CLASSES_ROOT,
                    ext_key_path,
                    0,
                    winreg.KEY_WRITE
                )
                
                # Добавляем "Сжать"
                try:
                    compress_key = winreg.CreateKey(ext_key, 'Сжать')
                except FileExistsError:
                    compress_key = winreg.OpenKey(ext_key, 'Сжать', 0, winreg.KEY_WRITE)
                
                try:
                    command_key = winreg.CreateKey(compress_key, 'command')
                except FileExistsError:
                    command_key = winreg.OpenKey(compress_key, 'command', 0, winreg.KEY_WRITE)
                
                winreg.SetValueEx(command_key, '', 0, winreg.REG_SZ, compress_command)
                winreg.CloseKey(command_key)
                winreg.CloseKey(compress_key)
                
                # Добавляем "Конвертация" для видео
                try:
                    convert_key = winreg.CreateKey(ext_key, 'Конвертация')
                except FileExistsError:
                    convert_key = winreg.OpenKey(ext_key, 'Конвертация', 0, winreg.KEY_WRITE)
                
                try:
                    command_key = winreg.CreateKey(convert_key, 'command')
                except FileExistsError:
                    command_key = winreg.OpenKey(convert_key, 'command', 0, winreg.KEY_WRITE)
                
                winreg.SetValueEx(command_key, '', 0, winreg.REG_SZ, convert_command)
                winreg.CloseKey(command_key)
                winreg.CloseKey(convert_key)
                winreg.CloseKey(ext_key)
                
            except Exception as e:
                print(f"Предупреждение: Не удалось добавить для {ext}: {e}")
        
        print("✓ Пункт 'Сжать' добавлен для всех видео форматов")
        
        # Добавляем "Конвертация" для аудио
        for ext in audio_extensions:
            try:
                ext_key_path = f'{ext}\\shell'
                ext_key = winreg.OpenKey(
                    winreg.HKEY_CLASSES_ROOT,
                    ext_key_path,
                    0,
                    winreg.KEY_WRITE
                )
                
                try:
                    convert_key = winreg.CreateKey(ext_key, 'Конвертация')
                except FileExistsError:
                    convert_key = winreg.OpenKey(ext_key, 'Конвертация', 0, winreg.KEY_WRITE)
                
                try:
                    command_key = winreg.CreateKey(convert_key, 'command')
                except FileExistsError:
                    command_key = winreg.OpenKey(convert_key, 'command', 0, winreg.KEY_WRITE)
                
                winreg.SetValueEx(command_key, '', 0, winreg.REG_SZ, convert_command)
                winreg.CloseKey(command_key)
                winreg.CloseKey(convert_key)
                winreg.CloseKey(ext_key)
                
            except Exception as e:
                print(f"Предупреждение: Не удалось добавить для {ext}: {e}")
        
        print("✓ Пункт 'Конвертация' добавлен для всех аудио форматов")
        
        # Добавляем "Конвертация" для изображений
        for ext in image_extensions:
            try:
                ext_key_path = f'{ext}\\shell'
                ext_key = winreg.OpenKey(
                    winreg.HKEY_CLASSES_ROOT,
                    ext_key_path,
                    0,
                    winreg.KEY_WRITE
                )
                
                try:
                    convert_key = winreg.CreateKey(ext_key, 'Конвертация')
                except FileExistsError:
                    convert_key = winreg.OpenKey(ext_key, 'Конвертация', 0, winreg.KEY_WRITE)
                
                try:
                    command_key = winreg.CreateKey(convert_key, 'command')
                except FileExistsError:
                    command_key = winreg.OpenKey(convert_key, 'command', 0, winreg.KEY_WRITE)
                
                winreg.SetValueEx(command_key, '', 0, winreg.REG_SZ, convert_command)
                winreg.CloseKey(command_key)
                winreg.CloseKey(convert_key)
                winreg.CloseKey(ext_key)
                
            except Exception as e:
                print(f"Предупреждение: Не удалось добавить для {ext}: {e}")
        
        print("✓ Пункт 'Конвертация' добавлен для всех форматов изображений")
        # Добавляем "Сжать" для аудио
        for ext in audio_extensions:
            try:
                ext_key_path = f'{ext}\\shell'
                ext_key = winreg.OpenKey(
                    winreg.HKEY_CLASSES_ROOT,
                    ext_key_path,
                    0,
                    winreg.KEY_WRITE
                )
                
                try:
                    compress_key = winreg.CreateKey(ext_key, 'Сжать')
                except FileExistsError:
                    compress_key = winreg.OpenKey(ext_key, 'Сжать', 0, winreg.KEY_WRITE)
                
                try:
                    command_key = winreg.CreateKey(compress_key, 'command')
                except FileExistsError:
                    command_key = winreg.OpenKey(compress_key, 'command', 0, winreg.KEY_WRITE)
                
                winreg.SetValueEx(command_key, '', 0, winreg.REG_SZ, compress_command)
                winreg.CloseKey(command_key)
                winreg.CloseKey(compress_key)
                winreg.CloseKey(ext_key)
                
            except Exception as e:
                print(f"Предупреждение: Не удалось добавить для {ext}: {e}")
        
        print("✓ Пункт 'Сжать' добавлен для всех аудио форматов")
        
        # Добавляем "Сжать" для изображений
        for ext in image_extensions:
            try:
                ext_key_path = f'{ext}\\shell'
                ext_key = winreg.OpenKey(
                    winreg.HKEY_CLASSES_ROOT,
                    ext_key_path,
                    0,
                    winreg.KEY_WRITE
                )
                
                try:
                    compress_key = winreg.CreateKey(ext_key, 'Сжать')
                except FileExistsError:
                    compress_key = winreg.OpenKey(ext_key, 'Сжать', 0, winreg.KEY_WRITE)
                
                try:
                    command_key = winreg.CreateKey(compress_key, 'command')
                except FileExistsError:
                    command_key = winreg.OpenKey(compress_key, 'command', 0, winreg.KEY_WRITE)
                
                winreg.SetValueEx(command_key, '', 0, winreg.REG_SZ, compress_command)
                winreg.CloseKey(command_key)
                winreg.CloseKey(compress_key)
                winreg.CloseKey(ext_key)
                
            except Exception as e:
                print(f"Предупреждение: Не удалось добавить для {ext}: {e}")
        
        print("✓ Пункт 'Сжать' добавлен для всех форматов изображений")
        
        print("\nГотово! Теперь вы можете использовать:")
        print("  - 'Сжать' - для видео, аудио и изображений")
        print("  - 'Конвертация' - для фото, видео и аудио файлов")
        print("\nПерезапустите проводник Windows или перезагрузите компьютер для применения изменений.")
        
    except PermissionError:
        print("ОШИБКА: Недостаточно прав для изменения реестра!")
        print("Пожалуйста, запустите скрипт от имени администратора.")
        sys.exit(1)
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        sys.exit(1)


def delete_registry_key(parent_key, key_name):
    """Безопасное удаление ключа реестра"""
    try:
        # Пытаемся удалить дочерний ключ command, если он существует
        try:
            winreg.DeleteKey(parent_key, f'{key_name}\\command')
        except (FileNotFoundError, OSError):
            pass
        
        # Удаляем сам ключ
        try:
            winreg.DeleteKey(parent_key, key_name)
            return True
        except (FileNotFoundError, OSError):
            return False
    except Exception:
        return False


def remove_from_registry():
    """Удаляет записи из реестра Windows"""
    video_extensions = [
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', 
        '.flv', '.webm', '.m4v', '.3gp', '.mpg', '.mpeg'
    ]
    
    audio_extensions = [
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.ac3'
    ]
    
    image_extensions = [
        '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.webp', '.heic', '.heif'
    ]
    
    # Старые названия пунктов меню, которые нужно удалить
    old_menu_items = [
        'Сжать видео',
        'Сжать',
        'Конвертировать в MP4',
        'Конвертация'
    ]
    
    try:
        # Удаляем старые пункты для всех файлов
        base_key = r'*\shell'
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CLASSES_ROOT,
                base_key,
                0,
                winreg.KEY_WRITE | winreg.KEY_ENUMERATE_SUB_KEYS
            )
            
            for menu_item in old_menu_items:
                if delete_registry_key(key, menu_item):
                    print(f"✓ Пункт '{menu_item}' удален из контекстного меню для всех файлов")
            
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Ошибка при удалении из базового ключа: {e}")
        
        # Удаляем пункты для видео расширений
        removed_count = 0
        for ext in video_extensions:
            try:
                ext_key_path = f'{ext}\\shell'
                ext_key = winreg.OpenKey(
                    winreg.HKEY_CLASSES_ROOT,
                    ext_key_path,
                    0,
                    winreg.KEY_WRITE | winreg.KEY_ENUMERATE_SUB_KEYS
                )
                
                for menu_item in old_menu_items:
                    if delete_registry_key(ext_key, menu_item):
                        removed_count += 1
                
                winreg.CloseKey(ext_key)
            except Exception:
                pass
        
        if removed_count > 0:
            print(f"✓ Пункты удалены для видео форматов ({removed_count} записей)")
        
        # Удаляем пункты для аудио расширений
        removed_count = 0
        for ext in audio_extensions:
            try:
                ext_key_path = f'{ext}\\shell'
                ext_key = winreg.OpenKey(
                    winreg.HKEY_CLASSES_ROOT,
                    ext_key_path,
                    0,
                    winreg.KEY_WRITE | winreg.KEY_ENUMERATE_SUB_KEYS
                )
                
                for menu_item in old_menu_items:
                    if delete_registry_key(ext_key, menu_item):
                        removed_count += 1
                
                winreg.CloseKey(ext_key)
            except Exception:
                pass
        
        if removed_count > 0:
            print(f"✓ Пункты удалены для аудио форматов ({removed_count} записей)")
        
        # Удаляем пункты для изображений
        removed_count = 0
        for ext in image_extensions:
            try:
                ext_key_path = f'{ext}\\shell'
                ext_key = winreg.OpenKey(
                    winreg.HKEY_CLASSES_ROOT,
                    ext_key_path,
                    0,
                    winreg.KEY_WRITE | winreg.KEY_ENUMERATE_SUB_KEYS
                )
                
                for menu_item in old_menu_items:
                    if delete_registry_key(ext_key, menu_item):
                        removed_count += 1
                
                winreg.CloseKey(ext_key)
            except Exception:
                pass
        
        if removed_count > 0:
            print(f"✓ Пункты удалены для форматов изображений ({removed_count} записей)")
        
        print("\n✓ Очистка реестра завершена!")
        
    except PermissionError:
        print("ОШИБКА: Недостаточно прав для изменения реестра!")
        print("Пожалуйста, запустите скрипт от имени администратора.")
        sys.exit(1)
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Главная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == '--remove':
        print("Удаление пунктов из контекстного меню...")
        remove_from_registry()
    else:
        print("Добавление пунктов 'Сжать' (для видео/аудио/изображений) и 'Конвертация' (для фото/видео/аудио) в контекстное меню...")
        print("Убедитесь, что вы запускаете скрипт от имени администратора!")
        input("Нажмите Enter для продолжения...")
        add_to_registry()
    
    input("\nНажмите Enter для выхода...")


if __name__ == '__main__':
    main()
