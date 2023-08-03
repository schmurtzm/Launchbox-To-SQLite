import os
import sqlite3

def create_platform_database(platform):
    db_dir = "platform_databases"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    db_file = os.path.join(db_dir, f'{platform}.db')
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create Games table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Games (
                        Name TEXT,
                        DatabaseID INTEGER
                    )''')

    # Create Images table with ImageID as an auto-incremental unique ID
    cursor.execute('''CREATE TABLE IF NOT EXISTS Images (
                        ImageID INTEGER PRIMARY KEY AUTOINCREMENT,
                        DatabaseID INTEGER,
                        FileName TEXT,
                        Type TEXT,
                        Region TEXT
                    )''')

    conn.commit()
    conn.close()
    return db_file

# Connexion à la base de données principale
main_db_file = 'launchbox_database.db'
main_conn = sqlite3.connect(main_db_file)
main_cursor = main_conn.cursor()

# Récupérer les plateformes distinctes depuis la table Games
main_cursor.execute("SELECT DISTINCT Platform FROM Games")
platforms = main_cursor.fetchall()

# Fermer la connexion à la base de données principale
main_conn.close()

# Pour chaque plateforme, créer une base de données distincte
for platform in platforms:
    platform = platform[0]  # Extraire le nom de la plateforme de la tuple
    db_file = create_platform_database(platform)

    # Connexion à la base de données de la plateforme actuelle
    platform_conn = sqlite3.connect(db_file)
    platform_cursor = platform_conn.cursor()

    # Requête optimisée pour remplir la table Games dans la nouvelle base de données
    main_conn = sqlite3.connect(main_db_file)
    main_cursor = main_conn.cursor()
    main_cursor.execute('''SELECT Name, DatabaseID FROM Games WHERE Platform=?''', (platform,))
    games_data = main_cursor.fetchall()

    # Fermer la connexion à la base de données principale
    main_conn.close()

    # Insérer les données de la table Games dans la nouvelle base de données
    platform_cursor.executemany("INSERT INTO Games (Name, DatabaseID) VALUES (?, ?)", games_data)

    # Requête optimisée pour remplir la table Images dans la nouvelle base de données
    main_conn = sqlite3.connect(main_db_file)
    main_cursor = main_conn.cursor()
    main_cursor.execute('''SELECT DatabaseID, FileName, Type, Region FROM Images WHERE DatabaseID IN (
                            SELECT DatabaseID FROM Games WHERE Platform=?
                        )''', (platform,))
    images_data = main_cursor.fetchall()

    # Fermer la connexion à la base de données principale
    main_conn.close()

    # Insérer les données de la table Images dans la nouvelle base de données
    platform_cursor.executemany("INSERT INTO Images (DatabaseID, FileName, Type, Region) VALUES (?, ?, ?, ?)", images_data)

    platform_conn.commit()
    platform_conn.close()