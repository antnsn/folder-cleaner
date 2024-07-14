import os
import shutil
import logging
import argparse

def organize_files(path):
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # List of folder names corresponding to file categories
    folder_names = [
        'Misc Files', 'Developer Files', 'Disk Image Files', 'Compressed Files',
        'Settings Files', 'System Files', 'Plugin Files', 'Web Files', 'Game Files',
        'Database', 'Spreadsheet', '3D', 'Images', 'Text Files', 'Executables',
        'Videos', 'Music', 'PDF', 'Presentation', 'Data Files', 'E-mail Files'
    ]

    # List of file extensions for each category
    file_categories = {
        'Images': ['.heic', '.png', '.jpg', '.tif', '.tiff', '.bmp', '.jpeg', '.gif', '.eps', '.raw', '.cr2', '.nef', '.orf', '.sr2'],
        'Text Files': ['.txt', '.fpt', '.docx', '.rtf', '.log', '.doc', '.pfx', '.cer'],
        'Presentation': ['.ppt', '.pptx'],
        'Data Files': ['.csv', '.key', '.keychain', '.dat', '.sdf', '.tar', '.xml', '.vcf'],
        'Music': ['.flac','.aif', '.iff', '.m3u', '.m4a', '.mid', '.mp3', '.mpa', '.wav', '.wma'],
        'Videos': ['.3g2', '.3gp', '.asf', '.avi', '.flv', '.m4v', '.mov', '.mp4', '.mpg', '.rm', '.srt', '.swf', '.mkv', '.vob', '.wmv'],
        '3D': ['.3dm', '.3ds', '.max', '.obj', '.stl', '.3mf'],
        'Spreadsheet': ['.xlr', '.xls', '.xlsx'],
        'Database': ['.db', '.sql', '.accdb', '.dbf', '.mdb', '.pdb'],
        'Executables': ['.exe', '.msi', '.apk', '.app', '.bat', '.cgi', '.com', '.gadget', '.jar', '.wsf'],
        'Game Files': ['.b', '.dem', '.gam', '.nes', '.rom', '.sav'],
        'PDF': ['.pdf'],
        'Web Files': ['.asp', '.aspx', '.css', '.htm', '.html', '.js', '.jsp', '.php', '.rss', '.webp'],
        'Plugin Files': ['.crx', '.plugin', '.fnt', '.fon', '.otf', '.ttf'],
        'System Files': ['.cab', '.deskthemepack', '.dll', '.ico', '.sys', '.lnk', '.dmp', '.drv'],
        'Settings Files': ['.ini', '.cfg', '.prf'],
        'Compressed Files': ['.7z', '.cbr', '.deb', '.gz', '.pkg', '.rar', '.rpm', '.tar.gz', '.zip', '.zipx'],
        'Disk Image Files': ['.bin', '.dmg', '.iso', '.img', '.mdf', '.vcd', '.svg'],
        'Developer Files': ['.c', '.class', '.cpp', '.cs', '.java', '.pl', '.py', '.sh', '.vb', '.vcxproj', '.jsp', '.servlet', '.yaml', '.yml', '.ps1', '.json'],
        'Misc Files': ['.ics', '.part', '.torrent'],
        'E-mail Files': ['.eml']
    }

    # Dictionary to track which folders need to be created
    folders_to_create = {folder: False for folder in folder_names}

    # Determine which folders need to be created and move files
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file)[1].lower()  # Get the file extension and convert to lowercase
            for category, extensions in file_categories.items():
                if file_ext in extensions:
                    if not folders_to_create[category]:
                        os.makedirs(os.path.join(path, category), exist_ok=True)
                        folders_to_create[category] = True
                    try:
                        shutil.move(file_path, os.path.join(path, category, file))
                        logging.info(f"Moved file {file} to {category} folder.")
                    except Exception as e:
                        logging.error(f"Error moving file {file}: {e}")
                    break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files into folders by type.")
    parser.add_argument("--path", type=str, required=True, help="The path of the directory to organize.")
    args = parser.parse_args()
    
    organize_files(args.path)
