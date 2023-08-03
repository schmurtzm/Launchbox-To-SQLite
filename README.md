## Launchbox Database Conversion to SQLite

These scripts are mainly dedicated to Onion OS image scraper so only data related to images are exported.

`01-convert-to-SQLite.py` script allows you to convert Launchbox database from its original JSON format to a SQLite database. This conversion makes it faster and easier to query the data using SQLite.

`02-split-database-by-platform.py` splits the resulting database from the first script into separate databases based on distinct platforms for using it on low memory devices like the Miyoo Mini.

### Requirements

Before running the script, ensure you have the following installed:

- Python (3.6 or higher)
- sqlite3 module (should be included in the standard library)
- xml.etree.ElementTree module (should be included in the standard library)

### How it Works

The script reads game data from a Launchbox XML file and organizes it into two separate tables in a SQLite database: `Games` and `Images`.

#### Games Table

The `Games` table stores information about the games. It contains three columns:

- `Name`: The name of the game.
- `DatabaseID`: A unique identifier for the game.
- `Platform`: The platform on which the game is available. (platform field is not available once splitter as the name of the database is the platform)

The script filters out certain platforms that are not relevant to the target database. You can find the list of filtered platforms in the `filtered_platforms` set within the script. (for Onion we filter modern platforms)
If a game's platform is in this set, the game is skipped during the conversion process.

Additionally, the script replaces any unsupported characters (e.g., `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) in the game's name and platform with spaces to ensure easier search later.

#### Images Table

The `Images` table stores information about the game images. It has four columns:

- `ImageID`: An auto-incremental unique ID for the image (primary key).
- `DatabaseID`: The unique identifier of the game to which the image belongs.
- `FileName`: The name of the image file.
- `Type`: The type of image (e.g., Banner, Box - 3D, Screenshot - Gameplay, etc.).
- `Region`: The region associated with the image (if available).

The script also filters out certain image types that are not needed for the target database. You can find the list of filtered image types in the `filtered_image_types` set within the script. Images of these types are excluded from the conversion.

### Usage

To use the script, follow these steps:

1. Ensure you have Python installed on your system.
2. Download the `Metadata.xml` file from Launchbox, which contains the game data in XML format.
3. Save the script in the same directory as the `Metadata.xml` file.
4. Open a terminal or command prompt in the script's directory.
5. Run the script by executing the following command:


```python 01-convert-to-SQLite.py```

then to split the database :

```python 02-split-database-by-platform.py```

After running the script, a new SQLite database file named `launchbox_database.db` will be created in the same directory. This file will contain the converted data from the Launchbox XML file.

### Dev tips

[DB Browser for SQLite](https://sqlitebrowser.org/) is an awesome tool to browse your SQLite databases.


Request example to display 'Box - Front' image names of games called aerobiz with a priority on certain regions :

```SQL
SELECT * FROM Games JOIN Images ON Games.DatabaseID = Images.DatabaseID WHERE Games.Name LIKE '%aerobiz%' AND Images.Type = 'Box - Front'  
ORDER BY CASE WHEN Region = '' THEN 1
              WHEN Region = 'World' THEN 2
              WHEN Region = 'United States' THEN 3
              WHEN Region = 'North America' THEN 4
              WHEN Region = 'Europe' THEN 5
              ELSE 6 
              END
```
Display all the regions available : 

```SQL
select DISTINCT Region from Images
```
Display all the media types available : 

```SQL
select DISTINCT Type from Images
```


### Contributing

Contributions to this script are welcome! If you find any issues or have ideas for improvements, feel free to create an issue or submit a pull request on the GitHub repository.

### License

This project is licensed under the MIT License. You are free to use, modify, and distribute the script as per the terms of the license. Just mention the source and author please.

------------------------------------------------


 ## Contributing

Contributions to this script are welcome! If you find any issues or have ideas for improvements, feel free to create an issue or submit a pull request on the GitHub repository.
Do not hesitate, **Participate**, there are many ways :
- Join my Patreon community and be a part of supporting the development of my various projects!  [![Participate to my Patreon][Patreon-shield]][patreon]
  
- Or you can buy me a coffee to keep me awake during night coding sessions :dizzy_face: !
   <a href="https://www.buymeacoffee.com/schmurtz"><img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg" alt="Buy me a coffee" width="100"/></a>
<br/><br/>
Your contributions make a huge difference in keeping these projects alive !


[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/schmurtz
[Patreon-shield]:https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white
[patreon]: https://www.patreon.com/schmurtz


 ===========================================================================
