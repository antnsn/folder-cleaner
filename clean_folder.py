import os
import shutil
import json
import argparse
import openai
import logging
import sys


# Configure logging
logging.basicConfig(
    filename='file_organizer.log',  # Log file path
    level=logging.INFO,              # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Also print to stdout for Task Scheduler capture
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


class FileOrganizer:
    def __init__(self, path, api_key):
        self.path = path
        self.existing_folders = []
        self.files = []
        self.client = openai
        openai.api_key = api_key  # Ensure API key is set
        logging.info(f"Initialized FileOrganizer for path: {self.path}")

    def scan_directory(self):
        """Scan only the root directory for files and folders."""
        logging.info(f"Scanning directory: {self.path}")
        try:
            self.existing_folders = [
                item for item in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, item))
            ]
            self.files = [
                {
                    "name": file,
                    "path": os.path.join(self.path, file),
                    "extension": os.path.splitext(file)[1].lower(),
                }
                for file in os.listdir(self.path)
                if os.path.isfile(os.path.join(self.path, file))
            ]
            logging.info(f"Found {len(self.files)} files and {len(self.existing_folders)} folders.")
        except Exception as e:
            logging.error(f"Error scanning directory {self.path}: {e}")

    def generate_file_structure_json(self):
        """Generate a JSON structure of the directory."""
        logging.info(f"Generating file structure JSON for {self.path}")
        file_structure = {
            "path": self.path,
            "existing_folders": self.existing_folders,
            "files": self.files,
        }
        try:
            with open("file_structure.json", "w") as f:
                json.dump(file_structure, f, indent=4)
            logging.info("File structure JSON saved successfully.")
        except Exception as e:
            logging.error(f"Error generating file structure JSON: {e}")
        return file_structure

    def analyze_with_chatgpt(self, file_structure):
        """Use ChatGPT to suggest folder structures and file categorization in JSON format."""
        prompt = (
            "Please analyze the following directory structure represented in JSON format. "
            "Based on the file names and their extensions, suggest an organization plan in JSON format. "
            "For each file, return the file name and the recommended folder as a key-value pair. \n\n"
            "Here is the directory structure:\n"
            f"{json.dumps(file_structure, indent=4)}\n\n"
            "Please ensure that the output is valid JSON and follows this structure:\n"
            "{\n    \"file_name\": \"recommended_folder\"\n}"
        )

        try:
            response = self.client.chat.completions.create(model="gpt-4",  
                messages=[{"role": "user", "content": prompt}])
            logging.info(f"OpenAI response received successfully.")

            content = response.choices[0].message.content.strip()
            logging.info(f"Raw content received: {content}")

            if not content:
                logging.error("Received empty response from OpenAI.")
                return {}

            # Extract the JSON part from the response
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_content = content[json_start:json_end]

            # Attempt to parse the cleaned content as JSON
            return json.loads(json_content)

        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON response: {e}")
            return {}
        except Exception as e:
            logging.error(f"Error analyzing with ChatGPT: {e}")
            return {}

    def apply_organization_plan(self, organization_plan):
        """Apply the organization plan from ChatGPT."""
        try:
            # organization_plan should be a dictionary already
            for file in self.files:
                target_folder = organization_plan.get(file["name"])
                if target_folder:
                    target_path = os.path.join(self.path, target_folder)
                    os.makedirs(target_path, exist_ok=True)
                    shutil.move(file["path"], os.path.join(target_path, os.path.basename(file["path"])))
                    logging.info(f"Moved file {file['name']} to {target_folder} folder.")
                else:
                    logging.warning(f"No folder found for file {file['name']}.")
        except Exception as e:
            logging.error(f"Error applying organization plan: {e}")

    def organize(self):
        """Main method to organize files."""
        logging.info("Starting file organization process.")
        self.scan_directory()
        
        # Check if there are any files to organize
        if not self.files:
            logging.warning("No files found to organize. Aborting operation.")
            return  # Exit early if no files are found
        
        file_structure = self.generate_file_structure_json()
        organization_plan = self.analyze_with_chatgpt(file_structure)
        
        if organization_plan:
            self.apply_organization_plan(organization_plan)
            logging.info("File organization process completed.")
        else:
            logging.error("No valid organization plan received. Aborting operation.")


if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Organize files into folders by type.")
    parser.add_argument("--path", type=str, required=True, help="The path of the directory to organize.")
    parser.add_argument("--api_key", type=str, required=True, help="OpenAI API key.")
    args = parser.parse_args()

    # Initialize and run the organizer
    organizer = FileOrganizer(args.path, args.api_key)
    organizer.organize()
