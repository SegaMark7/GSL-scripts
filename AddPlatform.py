import os

# Получаем текущий каталог
current_directory = "."

# Проходим по всем файлам в текущем каталоге
for filename in os.listdir(current_directory):
    # Если файл имеет расширение .pce или .png, добавляем "-SuperGrafx" к его имени
    if filename.lower().endswith(('.pce', '.png')):
        new_filename = filename.split('.')[0] + '-SuperGrafx.' + filename.split('.')[-1]
        os.rename(filename, new_filename)
