import math
import sqlite3
import pandas as pd
import os


# Пути
current_path = os.getcwd() # Получение текущей директории
drive_path, cur_dir = os.path.splitdrive(current_path) # Получение текущего диска(HDD)
cores_path = drive_path + '\\retro_lib\\'
infos_path = drive_path + '\\retro_lib\\'
minigui_path = drive_path + '\\minigui\\'
shell_path = minigui_path + 'start_game.sh'
timer_path = '/sdcard/game/'

# Переменные
cores=[]
# DirMatch={
#     "folders":[],
#     "suffixes":[],
#     "cores":[]
# }

# Функции
def ReadShell():
    emu_num=0    
    with open(shell_path, encoding='utf-8') as file:
        for line in file:
            if 'case' in line:
                for line in file:
                    
                    if f'{emu_num})' in line:
                        for line in file:
                            if ';;' in line:
                                break
                            elif 'GAME_LIB' in line:
                                cores.append(line.split('=')[1].strip())
                                # DirMatch["cores"].append(line.split('=')[1].strip())

                    emu_num += 1
            elif 'esac' in line:
                return                   

def WriteDB():
    conn = sqlite3.connect('DirMatch.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match (
            coreid INTEGER PRIMARY KEY AUTOINCREMENT,
            folder CHAR(50),
            suffixes CHAR(50),
            cores CHAR(50)
        )
    ''')
    for core in cores:
        cursor.execute('''
        INSERT INTO match (folder, suffixes, core_name)
        VALUES (?, ?, ?)
        ''', (core_name, core_name, core))
    conn.commit()
    conn.close()

def ReadDB():
    conn = sqlite3.connect('DirMatch.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM match
    ''')
    for row in cursor:
        print(row)
    conn.close()

def ReadInfo():
    for core in DirMatch["cores"]:
       file_path=infos_path+core.split('.')[0]+'.info'
       if os.path.exists(file_path):
            with open(file_path, encoding='utf-8') as file:
                for line in file:
                    if 'supported_extensions' in line:
                        exts = line.split('=')[1].strip().replace('"', '')
                        DirMatch['suffixes'] = [f".{substr}" for substr in exts.split("|")]
            
def Insert_tbl_lg(lg, gameid, game):
    cursor.execute('''
                INSERT INTO tbl_? (en_id, en_title)
                VALUES (?, ?)
                ''', (lg, gameid, game))
    

def Insert_tbl_path():
    cursor.execute('''
        INSERT INTO tbl_path (path_id, path)
        SELECT ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM tbl_path)
        ''', (1, '/sdcard/game/'))
    
def Delete_tbls():
    # Получите список всех таблиц в базе данных, используя запрос
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
         cursor.execute(f"DELETE FROM {table[0]}")

def Create_tbls():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_en (
            en_id INTEGER PRIMARY KEY AUTOINCREMENT,
            en_title CHAR(50)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_game (
            gameid INTEGER PRIMARY KEY AUTOINCREMENT,
            game CHAR(50),
            suffix CHAR(5),
            zh_id INTEGER,
            en_id INTEGER,
            ko_id INTEGER,
            video_id INTEGER,
            class_type INTEGER,
            game_type INTEGER,
            hard INTEGER,
            timer CHAR(50)
        );
    ''')            
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_ko (
            ko_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ko_title CHAR(50)
        );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tbl_match (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        zh_match CHAR(50)
    );    
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tbl_path (
        path_id TEXT,
        path TEXT
    );    
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tbl_total (
        ID INTEGER,
        total INTEGER
    );    
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tbl_tw (
        en_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        en_title CHAR(50)
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tbl_video (
        video_id TEXT, 
        video TEXT, 
        path_id TEXT
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tbl_zh (
        zh_id INTEGER PRIMARY KEY AUTOINCREMENT,
        zh_title CHAR(50) 
    );
    ''')

if __name__ == '__main__':
    # Подключение к базе данных
    conn = sqlite3.connect('games.db')
    cursor = conn.cursor()

    Delete_tbls()

    Create_tbls()

    Insert_tbl_path()

    # узнаем последний элемент в таблице tbl_game
    cursor.execute('SELECT MAX(gameid) FROM tbl_game')
    gameid = cursor.fetchone()[0] or 0
    hard=0

    df = pd.read_excel('Match.xlsx')
    for index, row in df.iterrows():

        if row.coreid == '' and  row.coreid != row.coreid:
            break

        if row.folders != '' and row.folders == row.folders:        
            subdir_path = os.path.join(current_path, row.folders)
            suffixes = [f".{x.replace(' ', '')}" if not x.startswith(".") else x for x in row.suffixes.split('|')]
            if not os.path.exists(subdir_path):
                print(f'не существует папки: {subdir_path} ')
                continue
            for root, dirs, files in os.walk(subdir_path):
                for file in files:
                    if any(file.lower().endswith(s) for s in suffixes): 
                        gameid += 1
                        game = file[:file.rfind(".")]
                        suffix = os.path.splitext(file)[-1]
                        zh_id = en_id = ko_id = video_id = gameid
                        class_type = game_type = row.coreid
                        timer = timer_path + root[root.find(row.folders):].replace("\\", "/")
                        cursor.execute('''
                        INSERT INTO tbl_en (en_id, en_title)
                        VALUES (?, ?)
                        ''', (gameid, game))
                        cursor.execute('''
                        INSERT INTO tbl_game (gameid, game, suffix, zh_id, en_id, ko_id, video_id, class_type, game_type, hard, timer)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (gameid, game, suffix, zh_id, en_id, ko_id, video_id, class_type, game_type, hard, timer))
                        cursor.execute('''
                        INSERT INTO tbl_ko (ko_id, ko_title)
                        VALUES (?, ?)
                        ''', (gameid, game))
                        cursor.execute('''
                        INSERT INTO tbl_match (ID, zh_match)
                        VALUES (?, ?)
                        ''', (gameid, game.lower().replace(" ", "")))
                        cursor.execute('''
                        INSERT INTO tbl_tw (en_id, en_title)
                        VALUES (?, ?)
                        ''', (gameid, game))
                        cursor.execute('''
                        INSERT INTO tbl_video (video_id, video, path_id)
                        VALUES (?, NULL ,?)
                        ''', (gameid, 1))
                        cursor.execute('''
                        INSERT INTO tbl_zh (zh_id, zh_title)
                        VALUES (?, ?)
                        ''', (gameid, game))


    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()
    print('Обновление завершено')