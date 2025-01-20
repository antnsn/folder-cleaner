# Folder Cleaner

## Overview
The Folder Cleaner is a Python script designed to organize files in a specified directory based on their extensions. It utilizes the OpenAI API to generate an organization plan, categorizing files into appropriate folders for better management and accessibility.

## Features
- Automatically organizes files based on their extensions.
- Integrates with OpenAI's API to suggest folder structures.
- Handles sensitive files securely by recommending their relocation to secure directories.
- Logs all operations and responses for debugging and auditing purposes.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/folder-cleaner.git
   cd folder-cleaner
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
Run the script by specifying the target directory you want to clean and your OpenAI API key:
```bash
python clean_folder.py --path D:\Downloads --api_key your_api_key_here
```

### Command-Line Arguments
- `--directory`: The path to the directory containing the files to be organized. (Required)
- `--help`: Show help message and exit.

## Logging
The script logs all HTTP requests and responses from the OpenAI API, along with any errors encountered during execution. Check the `file_organizer.log` for detailed logs.

## Error Handling
If the script encounters issues with JSON parsing or API responses, it will attempt to clean up the response and reprocess it. Errors are logged for further investigation.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License.