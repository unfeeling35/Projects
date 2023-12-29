import os
import shutil
import zipfile


def normalize(file_name):
    cyrillic_to_latin = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'ґ': 'g',
        'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
        'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': "'", 'ю': 'iu', 'я': 'ia',
    }

    result = []
    base_name, extension = os.path.splitext(file_name)
    for char in base_name:
        if char.isalnum():
            result.append(char.lower())
        elif char in cyrillic_to_latin:
            result.append(cyrillic_to_latin[char])
        else:
            result.append('_')  #Замена на "_"

    return ''.join(result) + extension




def organize_files(folder_path):
    folders = ['images', 'documents', 'audio', 'video', 'archives', 'other']

    for folder in folders:
        if not os.path.exists(os.path.join(folder_path, folder)):
            os.makedirs(os.path.join(folder_path, folder)) #создание папок если их нету

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.startswith('.') or os.path.isdir(file_path) or file_name in folders:
            continue

        normalized_name = normalize(file_name)

        file_extension = os.path.splitext(file_name)[1][1:]

        if file_extension in ['jpeg', 'png', 'jpg', 'svg']:
            shutil.move(file_path, os.path.join(folder_path, 'images', normalized_name))
        elif file_extension in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
            shutil.move(file_path, os.path.join(folder_path, 'documents', normalized_name))
        elif file_extension in ['mp3', 'ogg', 'wav', 'amr']:
            shutil.move(file_path, os.path.join(folder_path, 'audio', normalized_name))
        elif file_extension in ['avi', 'mp4', 'mov', 'mkv']:
            shutil.move(file_path, os.path.join(folder_path, 'video', normalized_name))
        elif file_extension in ['zip', 'gz', 'tar']:
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(folder_path, 'archives', normalized_name))
                os.remove(file_path)  # удаление архива после распаковки
            except zipfile.BadZipFile:
                os.remove(file_path)
        else:
            shutil.move(file_path, os.path.join(folder_path, 'other', normalized_name))

    for folder in folders:
        folder_to_check = os.path.join(folder_path, folder)
        if os.path.exists(folder_to_check) and not os.listdir(folder_to_check):
            os.rmdir(folder_to_check) # удаление пустых папок



def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        sys.exit(1)

    organize_files(folder_path)
    print("Folder sorting completed successfully.")

if __name__ == "__main__":
    main()

