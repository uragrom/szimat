#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Универсальный скрипт для сжатия файлов (видео, аудио, изображения)
Использует ffmpeg для сжатия
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path


def find_ffmpeg():
    """Поиск ffmpeg в системе"""
    # Проверяем, установлен ли ffmpeg в PATH
    ffmpeg_in_path = shutil.which('ffmpeg')
    if ffmpeg_in_path:
        return ffmpeg_in_path
    
    # Получаем папку, где находится скрипт
    try:
        script_dir = Path(__file__).parent.absolute().resolve()
    except:
        script_dir = Path.cwd()
    
    # Проверяем папку проекта (где находится скрипт)
    project_paths = [
        script_dir / 'ffmpeg.exe',
        script_dir / 'ffmpeg' / 'ffmpeg.exe',
        script_dir / 'ffmpeg' / 'bin' / 'ffmpeg.exe',
    ]
    
    for path in project_paths:
        if path.exists():
            return str(path)
    
    # Также проверяем все файлы в папке проекта
    try:
        for item in script_dir.iterdir():
            if item.is_file():
                name_lower = item.name.lower()
                if name_lower == 'ffmpeg.exe' or name_lower == 'ffmpeg':
                    return str(item)
    except:
        pass
    
    # Проверяем возможные стандартные пути установки
    possible_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\ffmpeg\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\ffmpeg.exe',
        r'C:\Program Files (x86)\ffmpeg\ffmpeg.exe',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def compress_video(input_path, output_path, quality='medium'):
    """
    Сжимает видео файл используя ffmpeg
    
    Args:
        input_path: Путь к исходному видео
        output_path: Путь для сохранения сжатого видео
        quality: Качество сжатия ('low', 'medium', 'high')
    """
    ffmpeg_path = find_ffmpeg()
    
    if not ffmpeg_path:
        script_dir = Path(__file__).parent.absolute().resolve()
        print("="*60)
        print("ОШИБКА: ffmpeg не найден!")
        print("="*60)
        print(f"\nИспользуемый Python: {sys.executable}")
        print(f"Папка проекта: {script_dir}")
        print("\nПожалуйста, установите ffmpeg:")
        print("1. Скачайте с https://ffmpeg.org/download.html")
        print("2. Распакуйте и добавьте в PATH")
        print(f"3. Или поместите ffmpeg.exe в папку проекта: {script_dir}")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    # Параметры сжатия в зависимости от качества
    quality_settings = {
        'low': {
            'crf': '28',
            'preset': 'fast',
            'scale': '1280:-2'
        },
        'medium': {
            'crf': '23',
            'preset': 'medium',
            'scale': '1920:-2'
        },
        'high': {
            'crf': '18',
            'preset': 'slow',
            'scale': '1920:-2'
        }
    }
    
    settings = quality_settings.get(quality, quality_settings['medium'])
    
    # Команда ffmpeg для сжатия
    cmd = [
        ffmpeg_path,
        '-i', input_path,
        '-c:v', 'libx264',
        '-crf', settings['crf'],
        '-preset', settings['preset'],
        '-vf', f"scale={settings['scale']}",
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        '-y',  # Перезаписать выходной файл, если существует
        output_path
    ]
    
    try:
        print(f"Сжатие видео: {os.path.basename(input_path)}")
        print("Это может занять некоторое время...")
        
        # Запускаем ffmpeg
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Ждем завершения
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            input_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
            output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            compression_ratio = (1 - output_size / input_size) * 100
            
            print(f"\n✓ Видео успешно сжато!")
            print(f"  Исходный размер: {input_size:.2f} MB")
            print(f"  Новый размер: {output_size:.2f} MB")
            print(f"  Сжатие: {compression_ratio:.1f}%")
            print(f"  Файл сохранен: {output_path}")
        elif 'Permission denied' in stderr or 'Отказано в доступе' in stderr:
            # Пробуем сохранить в папку Temp
            fallback_path = generate_output_filename_in_temp(input_path)
            print("\nВ исходную папку записать не удалось (нет прав или файл открыт).")
            print(f"Повторная попытка: сохранение в {fallback_path}")
            cmd[-1] = fallback_path
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                input_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
                output_size = os.path.getsize(fallback_path) / (1024 * 1024)  # MB
                compression_ratio = (1 - output_size / input_size) * 100
                print(f"\n✓ Видео успешно сжато!")
                print(f"  Исходный размер: {input_size:.2f} MB")
                print(f"  Новый размер: {output_size:.2f} MB")
                print(f"  Сжатие: {compression_ratio:.1f}%")
                print(f"  Файл сохранён в папку Temp:")
                print(f"  {fallback_path}")
            else:
                print(f"ОШИБКА при сжатии видео:")
                print(stderr)
                print("\nВозможные причины «Отказано в доступе»:")
                print("  • Закройте файл, если он открыт в плеере или редакторе")
                print("  • Запустите скрипт от имени администратора")
                print("  • Сохраните результат в другую папку (например, Рабочий стол)")
                input("\nНажмите Enter для выхода...")
                sys.exit(1)
        else:
            print(f"ОШИБКА при сжатии видео:")
            print(stderr)
            input("\nНажмите Enter для выхода...")
            sys.exit(1)
            
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")
        sys.exit(1)


def convert_video(input_path, output_path, output_format='mp4'):
    """
    Конвертирует видео файл в другой формат используя ffmpeg
    
    Args:
        input_path: Путь к исходному видео
        output_path: Путь для сохранения конвертированного видео
        output_format: Формат выходного файла ('mp4', 'avi', 'mov', 'mkv', 'webm')
    """
    ffmpeg_path = find_ffmpeg()
    
    if not ffmpeg_path:
        script_dir = Path(__file__).parent.absolute().resolve()
        print("="*60)
        print("ОШИБКА: ffmpeg не найден!")
        print("="*60)
        print(f"\nИспользуемый Python: {sys.executable}")
        print(f"Папка проекта: {script_dir}")
        print("\nПожалуйста, установите ffmpeg:")
        print("1. Скачайте с https://ffmpeg.org/download.html")
        print("2. Распакуйте и добавьте в PATH")
        print(f"3. Или поместите ffmpeg.exe в папку проекта: {script_dir}")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    # Параметры кодека в зависимости от формата
    format_settings = {
        'mp4': {
            'video_codec': 'libx264',
            'audio_codec': 'aac',
            'extra': ['-movflags', '+faststart']
        },
        'avi': {
            'video_codec': 'libx264',
            'audio_codec': 'mp3',
            'extra': []
        },
        'mov': {
            'video_codec': 'libx264',
            'audio_codec': 'aac',
            'extra': []
        },
        'mkv': {
            'video_codec': 'libx264',
            'audio_codec': 'aac',
            'extra': []
        },
        'webm': {
            'video_codec': 'libvpx-vp9',
            'audio_codec': 'libopus',
            'extra': []
        }
    }
    
    settings = format_settings.get(output_format.lower(), format_settings['mp4'])
    
    # Команда ffmpeg для конвертации
    cmd = [
        ffmpeg_path,
        '-i', input_path,
        '-c:v', settings['video_codec'],
        '-c:a', settings['audio_codec'],
        '-y',  # Перезаписать выходной файл, если существует
    ]
    
    # Добавляем дополнительные параметры
    cmd.extend(settings['extra'])
    cmd.append(output_path)
    
    try:
        print(f"Конвертация видео: {os.path.basename(input_path)}")
        print(f"Формат: {output_format.upper()}")
        print("Это может занять некоторое время...")
        
        # Запускаем ffmpeg
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Ждем завершения
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            input_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
            output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            
            print(f"\n✓ Видео успешно конвертировано!")
            print(f"  Исходный размер: {input_size:.2f} MB")
            print(f"  Новый размер: {output_size:.2f} MB")
            print(f"  Файл сохранен: {output_path}")
        else:
            print(f"ОШИБКА при конвертации видео:")
            print(stderr)
            input("\nНажмите Enter для выхода...")
            sys.exit(1)
            
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")
        sys.exit(1)


def compress_audio(input_path, output_path, quality='medium'):
    """Сжимает аудио файл"""
    ffmpeg_path = find_ffmpeg()
    
    if not ffmpeg_path:
        print("ОШИБКА: ffmpeg не найден!")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    # Параметры сжатия для аудио
    quality_settings = {
        'low': {'bitrate': '96k'},
        'medium': {'bitrate': '128k'},
        'high': {'bitrate': '192k'}
    }
    
    settings = quality_settings.get(quality, quality_settings['medium'])
    
    cmd = [
        ffmpeg_path, '-i', input_path,
        '-codec:a', 'libmp3lame',
        '-b:a', settings['bitrate'],
        '-y', output_path
    ]
    
    try:
        print(f"Сжатие аудио: {os.path.basename(input_path)}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            input_size = os.path.getsize(input_path) / (1024 * 1024)
            output_size = os.path.getsize(output_path) / (1024 * 1024)
            compression_ratio = (1 - output_size / input_size) * 100
            
            print(f"\n✓ Аудио успешно сжато!")
            print(f"  Исходный размер: {input_size:.2f} MB")
            print(f"  Новый размер: {output_size:.2f} MB")
            print(f"  Сжатие: {compression_ratio:.1f}%")
        else:
            print(f"ОШИБКА: {stderr}")
            input("\nНажмите Enter для выхода...")
            sys.exit(1)
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)


def compress_image(input_path, output_path, quality='medium'):
    """Сжимает изображение"""
    ffmpeg_path = find_ffmpeg()
    
    if not ffmpeg_path:
        print("ОШИБКА: ffmpeg не найден!")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    # Параметры сжатия для изображений
    quality_settings = {
        'low': {'qscale': '5'},
        'medium': {'qscale': '3'},
        'high': {'qscale': '2'}
    }
    
    settings = quality_settings.get(quality, quality_settings['medium'])
    
    # Определяем формат по расширению
    ext = Path(output_path).suffix.lower()
    if ext in ['.jpg', '.jpeg']:
        cmd = [ffmpeg_path, '-i', input_path, '-q:v', settings['qscale'], '-y', output_path]
    elif ext == '.png':
        cmd = [ffmpeg_path, '-i', input_path, '-compression_level', '6', '-y', output_path]
    elif ext == '.webp':
        cmd = [ffmpeg_path, '-i', input_path, '-quality', '80', '-y', output_path]
    else:
        cmd = [ffmpeg_path, '-i', input_path, '-y', output_path]
    
    try:
        print(f"Сжатие изображения: {os.path.basename(input_path)}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            input_size = os.path.getsize(input_path) / (1024 * 1024)
            output_size = os.path.getsize(output_path) / (1024 * 1024)
            compression_ratio = (1 - output_size / input_size) * 100
            
            print(f"\n✓ Изображение успешно сжато!")
            print(f"  Исходный размер: {input_size:.2f} MB")
            print(f"  Новый размер: {output_size:.2f} MB")
            print(f"  Сжатие: {compression_ratio:.1f}%")
        else:
            print(f"ОШИБКА: {stderr}")
            input("\nНажмите Enter для выхода...")
            sys.exit(1)
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)


def detect_file_type(file_path):
    """Определяет тип файла"""
    ext = Path(file_path).suffix.lower()
    
    video_ext = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.mpg', '.mpeg']
    audio_ext = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.ac3']
    image_ext = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.webp', '.heic', '.heif']
    
    if ext in video_ext:
        return 'video'
    elif ext in audio_ext:
        return 'audio'
    elif ext in image_ext:
        return 'image'
    return None


def compress_file(input_path, output_path=None, quality='medium'):
    """Универсальная функция сжатия файлов"""
    file_type = detect_file_type(input_path)
    
    if not file_type:
        print(f"ОШИБКА: Неподдерживаемый тип файла: {input_path}")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    if not output_path:
        output_path = generate_output_filename(input_path)
    
    if file_type == 'video':
        compress_video(input_path, output_path, quality)
    elif file_type == 'audio':
        compress_audio(input_path, output_path, quality)
    elif file_type == 'image':
        compress_image(input_path, output_path, quality)


def generate_output_filename(input_path):
    """
    Генерирует имя выходного файла с префиксом compresed001
    
    Args:
        input_path: Путь к исходному файлу
        
    Returns:
        Путь к выходному файлу
    """
    path = Path(input_path)
    directory = path.parent
    stem = path.stem
    suffix = path.suffix
    
    # Добавляем compresed001 перед расширением
    output_name = f"{stem}compresed001{suffix}"
    output_path = directory / output_name
    
    # Если файл уже существует, добавляем номер
    counter = 1
    while output_path.exists():
        output_name = f"{stem}compresed001_{counter}{suffix}"
        output_path = directory / output_name
        counter += 1
    
    return str(output_path)


def generate_output_filename_in_temp(input_path):
    """Генерирует путь для сохранения в папку Temp (если в исходной папке нет прав записи)."""
    path = Path(input_path)
    directory = Path(tempfile.gettempdir()) / "video_compressed"
    directory.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    suffix = path.suffix
    output_name = f"{stem}compresed001{suffix}"
    output_path = directory / output_name
    counter = 1
    while output_path.exists():
        output_name = f"{stem}compresed001_{counter}{suffix}"
        output_path = directory / output_name
        counter += 1
    return str(output_path)


def generate_convert_filename(input_path, output_format='mp4'):
    """
    Генерирует имя выходного файла для конвертации
    
    Args:
        input_path: Путь к исходному файлу
        output_format: Формат выходного файла
        
    Returns:
        Путь к выходному файлу
    """
    path = Path(input_path)
    directory = path.parent
    stem = path.stem
    
    # Меняем расширение на новый формат
    output_name = f"{stem}.{output_format.lower()}"
    output_path = directory / output_name
    
    # Если файл уже существует, добавляем номер
    counter = 1
    while output_path.exists():
        output_name = f"{stem}_{counter}.{output_format.lower()}"
        output_path = directory / output_name
        counter += 1
    
    return str(output_path)


def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        print("Использование: compress_video.py <путь_к_файлу>")
        print("Поддерживаются: видео, аудио, изображения")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # Проверяем существование файла
    if not os.path.exists(input_path):
        print(f"ОШИБКА: Файл не найден: {input_path}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    # Определяем тип файла
    file_type = detect_file_type(input_path)
    if not file_type:
        print(f"ОШИБКА: Неподдерживаемый тип файла: {input_path}")
        print("Поддерживаются: видео, аудио, изображения")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    # Генерируем имя выходного файла
    output_path = generate_output_filename(input_path)
    
    # Сжимаем файл
    compress_file(input_path, output_path, quality='medium')
    
    print("\nГотово!")
    input("Нажмите Enter для выхода...")


if __name__ == '__main__':
    main()
