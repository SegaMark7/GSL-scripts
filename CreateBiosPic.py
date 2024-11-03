import os
import shutil

# Получить текущую директорию
current_dir = os.getcwd()

# Получить список всех файлов в текущей директории
all_files = os.listdir(current_dir)

# Отфильтровать список файлов
filtered_files = [file_name for file_name in all_files if not file_name.endswith(('.py', '.png', '.jpg'))]

# копировать файл BIOS.png из предыдущей папки


source_file = r'..\..\BIOS.png'
source_file_ext = os.path.splitext(source_file)[1]

# Копировать файл BIOS.png в каждый файл в отфильтрованном списке
for file_name in filtered_files:
    # узнать расширение файла
    file_ext = os.path.splitext(file_name)[1]    
    new_file_name = file_name.replace(file_ext, source_file_ext)
    destination_file = os.path.join(current_dir, new_file_name)
    shutil.copy(source_file, destination_file)
