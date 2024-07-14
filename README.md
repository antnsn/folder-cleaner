# File Organizer Script

## Overview

This script organizes files in a specified directory into subfolders based on file types. It categorizes files into predefined folders, such as Images, Documents, Videos, etc., making your directory neat and easy to navigate.

## Usage

To run the script, use the following command in your terminal:

```bash
python clean_folder.py --path=/your/directory/path
```

### Example

```bash
python clean_folder.py --path=/mnt/e/Downloads/
```

## How It Works

1. **Scans the directory**: The script scans the specified directory for files.
2. **Categorizes files**: It checks the file extensions and matches them to predefined categories.
3. **Creates folders**: Creates the necessary folders if they don't already exist.
4. **Moves files**: Moves the files into their respective folders based on their extensions.