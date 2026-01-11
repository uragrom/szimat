#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Универсальный скрипт для конвертации файлов (фото, видео, аудио)
Использует ffmpeg для конвертации
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def find_ffmpeg():
    """Поиск ffmpeg в системе"""
    ffmpeg_in_path = shutil.which('ffmpeg')
    if ffmpeg_in_path:
        return ffmpeg_in_path
    
    try:
        script_dir = Path(__file__).parent.absolute().resolve()
    except:
        script_dir = Path.cwd()
    
    project_paths = [
        script_dir / 'ffmpeg.exe',
        script_dir / 'ffmpeg' / 'ffmpeg.exe',
        script_dir / 'ffmpeg' / 'bin' / 'ffmpeg.exe',
    ]
    
    for path in project_paths:
        if path.exists():
            return str(path)
    
    possible_paths = [
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\ffmpeg\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe',
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def detect_file_type(file_path):
    """Определяет тип файла: video, audio, image"""
    ext = Path(file_path).suffix.lower()
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.mpg', '.mpeg', '.ts', '.m2ts']
    audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.opus', '.ac3']
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.webp', '.heic', '.heif']
    
    if ext in video_extensions:
        return 'video'
    elif ext in audio_extensions:
        return 'audio'
    elif ext in image_extensions:
        return 'image'
    else:
        return None


def get_available_formats(file_type):
    """Возвращает доступные форматы для конвертации"""
    formats = {
        'video': ['mp4', 'avi', 'mov', 'mkv', 'webm', 'wmv', 'flv'],
        'audio': ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'opus'],
        'image': ['jpg', 'png', 'webp', 'bmp', 'tiff', 'gif']
    }
    return formats.get(file_type, [])


def show_format_menu(file_type, available_formats):
    """Показывает меню выбора формата"""
    print(f"\n{'='*60}")
    print(f"Конвертация {file_type.upper()}")
    print(f"{'='*60}")
    print("\nДоступные форматы для конвертации:")
    
    for i, fmt in enumerate(available_formats, 1):
        print(f"  {i}. {fmt.upper()}")
    
    while True:
        try:
            choice = input(f"\nВыберите формат (1-{len(available_formats)}) или 'q' для выхода: ").strip().lower()
            if choice == 'q':
                return None
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_formats):
                return available_formats[choice_num - 1]
            else:
                print("Неверный выбор! Попробуйте снова.")
        except ValueError:
            print("Неверный ввод! Введите число или 'q'.")


def convert_file(input_path, output_path, file_type, output_format):
    """Конвертирует файл в указанный формат"""
    ffmpeg_path = find_ffmpeg()
    
    if not ffmpeg_path:
        print("="*60)
        print("ОШИБКА: ffmpeg не найден!")
        print("="*60)
        print("\nПожалуйста, установите ffmpeg:")
        print("1. Скачайте с https://ffmpeg.org/download.html")
        print("2. Распакуйте и добавьте в PATH")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)
    
    # Параметры для разных типов файлов
    if file_type == 'video':
        cmd = [
            ffmpeg_path, '-i', input_path,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-movflags', '+faststart',
            '-y', output_path
        ]
    elif file_type == 'audio':
        if output_format == 'mp3':
            cmd = [ffmpeg_path, '-i', input_path, '-codec:a', 'libmp3lame', '-b:a', '192k', '-y', output_path]
        elif output_format == 'wav':
            cmd = [ffmpeg_path, '-i', input_path, '-codec:a', 'pcm_s16le', '-y', output_path]
        elif output_format == 'flac':
            cmd = [ffmpeg_path, '-i', input_path, '-codec:a', 'flac', '-y', output_path]
        elif output_format == 'aac':
            cmd = [ffmpeg_path, '-i', input_path, '-codec:a', 'aac', '-b:a', '192k', '-y', output_path]
        elif output_format == 'ogg':
            cmd = [ffmpeg_path, '-i', input_path, '-codec:a', 'libvorbis', '-y', output_path]
        elif output_format == 'm4a':
            cmd = [ffmpeg_path, '-i', input_path, '-codec:a', 'aac', '-b:a', '192k', '-y', output_path]
        elif output_format == 'opus':
            cmd = [ffmpeg_path, '-i', input_path, '-codec:a', 'libopus', '-y', output_path]
        else:
            cmd = [ffmpeg_path, '-i', input_path, '-y', output_path]
    elif file_type == 'image':
        cmd = [ffmpeg_path, '-i', input_path, '-y', output_path]
    else:
        print(f"ОШИБКА: Неподдерживаемый тип файла: {file_type}")
        sys.exit(1)
    
    try:
        print(f"\nКонвертация: {os.path.basename(input_path)}")
        print(f"Формат: {output_format.upper()}")
        print("Это может занять некоторое время...")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            input_size = os.path.getsize(input_path) / (1024 * 1024)  # MB
            output_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            
            print(f"\n✓ Файл успешно конвертирован!")
            print(f"  Исходный размер: {input_size:.2f} MB")
            print(f"  Новый размер: {output_size:.2f} MB")
            print(f"  Файл сохранен: {output_path}")
        else:
            print(f"ОШИБКА при конвертации:")
            print(stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def generate_output_filename(input_path, output_format):
    """Генерирует имя выходного файла"""
    path = Path(input_path)
    directory = path.parent
    stem = path.stem
    
    output_name = f"{stem}.{output_format.lower()}"
    output_path = directory / output_name
    
    counter = 1
    while output_path.exists():
        output_name = f"{stem}_{counter}.{output_format.lower()}"
        output_path = directory / output_name
        counter += 1
    
    return str(output_path)


def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        print("Использование: convert_video.py <путь_к_файлу>")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
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
    
    # Получаем доступные форматы
    available_formats = get_available_formats(file_type)
    
    if not available_formats:
        print(f"ОШИБКА: Нет доступных форматов для типа: {file_type}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    # Показываем меню выбора формата
    output_format = show_format_menu(file_type, available_formats)
    
    if not output_format:
        print("Конвертация отменена.")
        input("Нажмите Enter для выхода...")
        sys.exit(0)
    
    # Генерируем имя выходного файла
    output_path = generate_output_filename(input_path, output_format)
    
    # Конвертируем файл
    convert_file(input_path, output_path, file_type, output_format)
    
    print("\nГотово!")
    input("Нажмите Enter для выхода...")


if __name__ == '__main__':
    main()
