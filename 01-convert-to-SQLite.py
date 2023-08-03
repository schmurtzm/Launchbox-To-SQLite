import xml.etree.ElementTree as ET
import sqlite3
import re

def insert_game_data(cursor, data):
    name = data[0]
    name = re.sub(r'[\\/:\*\?"<>|]', ' ', name)  # Replace unsupported characters with spaces
    data[0] = name
    placeholders = ','.join(['?'] * len(data))
    cursor.execute('INSERT INTO Games (Name, DatabaseID, Platform) VALUES ({})'.format(placeholders), data)


def insert_image_data(cursor, data):
    placeholders = ','.join(['?'] * len(data))
    cursor.execute('INSERT INTO Images (DatabaseID, FileName, Type, Region) VALUES ({})'.format(placeholders), data)


def convert_xml_to_sqlite(xml_file, db_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create Games table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Games (
                        Name TEXT,
                        DatabaseID INTEGER,
                        Platform TEXT
                    )''')

    # Create Images table with ImageID as an auto-incremental unique ID
    cursor.execute('''CREATE TABLE IF NOT EXISTS Images (
                        ImageID INTEGER PRIMARY KEY AUTOINCREMENT,
                        DatabaseID INTEGER,
                        FileName TEXT,
                        Type TEXT,
                        Region TEXT
                    )''')

    # Parse XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    filtered_platforms = {
        "Sony Playstation 2",
        "Android",
        "Apple iOS",
        "Apple Mac OS",
        "Microsoft Xbox",
        "Microsoft Xbox 360",
        "Microsoft Xbox One",
        "Nintendo 3DS",
        "Nintendo 64",
        "Nintendo 64DD",
        "Nintendo DS",
        "Nintendo GameCube",
        "Nintendo Switch",
        "Nintendo Wii",
        "Nintendo Wii U",
        "Sega Dreamcast",
        "Sega Dreamcast VMU",
        "Sega Saturn",
        "Sega Triforce",
        "Sony Playstation 3",
        "Sony Playstation 4",
        "Sony Playstation 5",
        "Sony Playstation Vita",
        "Sony PSP",
        "Sony PSP Minis",
        "Web Browser"
    }

    filtered_image_types = {
        "Banner",
        "Box - 3D",
        "Box - Front",
        "Screenshot - Gameplay",
        "Screenshot - Game Title",
        "Clear Logo"
    }

    for game in root.findall('Game'):
        platform = game.find('Platform').text
        if platform in filtered_platforms:
            continue  # Skip adding the game if platform is in the filtered platforms list

        name = game.find('Name').text
        database_id = int(game.find('DatabaseID').text)

        # Transform platform names
        platform = re.sub(r'[\\/:\*\?"<>|]', ' ', platform)
        # if platform == "3DO Interactive Multiplayer":
            # platform = "3DO"
        # elif platform == "Sony Playstation":
            # platform = "PS"

        game_data = [name, database_id, platform]
        insert_game_data(cursor, game_data)

    # Insert Image data into Images table
    unique_ids = set()  # Keep track of unique DatabaseID values
    for image_elem in root.iter('GameImage'):
        database_id = int(image_elem.findtext('DatabaseID'))
        image_type = image_elem.findtext('Type')
        image_filename = image_elem.findtext('FileName')
        region = image_elem.findtext('Region')  # Add the Region value

        # Ensure each image is inserted only once for a given DatabaseID
        if image_type in filtered_image_types:
            image_data = [database_id, image_filename, image_type, region]
            insert_image_data(cursor, image_data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()


# Usage example
xml_file = 'Metadata.xml'
db_file = 'launchbox_database.db'
convert_xml_to_sqlite(xml_file, db_file)
