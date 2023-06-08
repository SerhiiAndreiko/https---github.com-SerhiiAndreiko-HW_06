import os
import shutil
import sys

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

# Функція для нормалізації імен
def normalize(file_name):
    # Транслітерація кирилиці на латиницю
    transliteration = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh',
        'З': 'Z', 'И': 'Y', 'І': 'Y', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
        'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '', 'Ю': 'Yu', 'Я': 'Ya'
    }

    normalized = ''
    file_name, extension = os.path.splitext(file_name)
    for char in file_name:
        if char.isalnum() or char == '.':
            normalized += char
        elif char in transliteration:
            normalized += transliteration[char]
        else:
            normalized += '_'
    normalized += '_'
    return normalized

def process_folder(folder_path):
    global known_extensions
    global unknown_extensions

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, extension = os.path.splitext(file_path)
            #extension = extension.upper()[1:]
            known_category = None

            for category, extensions in CATEGORIES.items():
                if extension.upper()[1:] in extensions:
                    known_category = category
                    break
            if known_category:
                known_extensions.append(extension)
                normalized_extension = extension.upper().lstrip('.')
                new_file_name = normalize(file[:file.rindex('.')]) + '.' + normalized_extension
                new_file_path = os.path.join(folder_path, known_category, new_file_name)
                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                shutil.move(file_path, new_file_path)
            
            
            
            #if known_category:
                #nown_extensions.append(extension)
                #new_file_path = os.path.normpath(os.path.join(folder_path, known_category, file))
                #os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                #shutil.move(file_path, new_file_path)
            else:
                unknown_extensions.append(extension)

    # Видаляємо порожні папки
    for root, dirs, _ in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Потрібно вказати шлях до папки.')
        sys.exit(1)

    target_folder = sys.argv[1]
    if not os.path.isdir(target_folder):
        print('Невірний шлях до папки.')
        sys.exit(1)

    # Створюємо папки для категорій, якщо вони ще не існують
    for category in CATEGORIES.keys():
        category_path = os.path.join(target_folder, category)
        os.makedirs(category_path, exist_ok=True)

    process_folder(target_folder)

    print('Список файлів в кожній категорії:')
    for category in CATEGORIES.keys():
        category_path = os.path.join(target_folder, category)
        files = os.scandir(category_path)
        print(f'{category}: {", ".join(file.name for file in files)}')


    print('Перелік усіх відомих розширень:')
    print(', '.join(set(known_extensions)))

    print('Перелік невідомих розширень:')
    print(', '.join(set(unknown_extensions)))