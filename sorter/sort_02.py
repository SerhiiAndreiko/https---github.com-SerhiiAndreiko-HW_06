import os
import shutil
import sys
from pathlib import Path
import zipfile
import tarfile

from sorter.normalize import normalize


# Список розширень для кожної категорії
CATEGORIES = {
    'images': ['.JPEG', '.PNG', '.JPG', '.SVG'],
    'videos': ['.AVI', '.MP4', '.MOV', '.MKV'],
    'documents': ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'],
    'audio': ['.MP3', '.OGG', '.WAV', '.AMR'],
    'archives': ['.ZIP', '.GZ', '.TAR']}
unknown_extensions = []
known_extensions = []

def create_category_folders(folder_path):
    for category in CATEGORIES.keys():
        category_folder = os.path.join(folder_path, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)



def get_category(extension):
    for category, extensions in CATEGORIES.items():
        if extension.upper() in extensions:
            return category
    return 'other'       
    



def process_folder(folder_path):

    path = Path(folder_path)
    
    for element in path.glob("**/*"):
    
        if element.is_file():
            file_name = element.stem
            extension = element.suffix
            known_category = get_category(extension)
            path.joinpath(known_category).mkdir(exist_ok=True)
            new_file_name = normalize(file_name) + extension
            new_file_path = path.joinpath(known_category, new_file_name)
            element.replace(new_file_path)
        elif element.is_dir():
            if not any(element.iterdir()):
                element.rmdir


def unpack_archives(folder_path):
    path = Path(folder_path)
    archives_folder = path.joinpath("archives")
    archives_folder.mkdir(exist_ok=True)
    
    for element in path.glob("**/*"):
        if element.is_file():
            extension = element.suffix
            if extension.upper() in CATEGORIES['archives']:
                archive_path = str(element)
                try:
                    with tarfile.open(archive_path, 'r') as tar:
                        tar.extractall(archives_folder)
                except tarfile.TarError:
                    print(f"Помилка розпакування архіву: {element}")
                except FileNotFoundError:
                    print(f"Файл не знайдено: {element}")
                else:
                    element.unlink()
            elif extension.lower() == '.zip':
                archive_path = str(element)
                try:
                    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                        zip_ref.extractall(archives_folder)
                except zipfile.BadZipFile:
                    print(f"Помилка розпакування архіву: {element}")
                except FileNotFoundError:
                    print(f"Файл не знайдено: {element}")
                else:
                    element.unlink()


def delete_empty_folders(folder_path):
    path = Path(folder_path)
    
    for element in path.glob("**/*"):
        if element.is_dir() and not any(element.iterdir()):
            element.rmdir()

def main():
    if len(sys.argv) < 2:
        print('Потрібно вказати шлях до папки.')
        sys.exit(1)

    target_folder = sys.argv[1]
    if not os.path.isdir(target_folder):
        print('Невірний шлях до папки.')
        sys.exit(1)

    delete_empty_folders(target_folder)
    create_category_folders(target_folder)
    process_folder(target_folder)
    unpack_archives(target_folder)
    print('Операція завершена успішно.')

if __name__ == '__main__':
    main()
    

