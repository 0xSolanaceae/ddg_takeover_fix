import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_manifest(manifest_path):
    try:
        with open(manifest_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Manifest file not found")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON: {e}")
        return None

def save_manifest(manifest_path, manifest_data):
    try:
        with open(manifest_path, 'w') as f:
            json.dump(manifest_data, f, indent=4)
    except IOError as e:
        logging.error(f"Error writing to file: {e}")

def patch_manifest(manifest_data):
    if "chrome_settings_overrides" in manifest_data:
        if "search_provider" in manifest_data["chrome_settings_overrides"]:
            if not manifest_data["chrome_settings_overrides"]["search_provider"].get("is_default", True):
                logging.info("Patch already applied, you're good to go.")
            else:
                manifest_data["chrome_settings_overrides"]["search_provider"]["is_default"] = False
                logging.info("Manifest patched.")
        else:
            logging.error("No search provider found in chrome_settings_overrides.")
    else:
        logging.error("No chrome_settings_overrides found in manifest.")
        
def main():
    manifest_path = input("Please enter the path to DDG's manifest.json file: ")

    if not os.path.exists(manifest_path):
        logging.error("Manifest file not found at the provided path.")
        return

    manifest_data = load_manifest(manifest_path)
    if manifest_data is None:
        return

    patch_manifest(manifest_data)
    save_manifest(manifest_path, manifest_data)

if __name__ == "__main__":
    main()