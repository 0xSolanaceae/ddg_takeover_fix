#!/usr/bin/env python3
import os
import json
import platform

def main():
    if platform.system() != "Windows":
        print("ERROR: This script is only supported on Windows.")
        return
    
    user = os.getlogin()

    print("If your browser is chromium based, like Google Chrome, Thorium, or Vivaldi, enter in 'chromium' below.")
    browser_selection = input("Select your browser (chromium/edge supported): ").lower()
    if browser_selection == 'chromium':
        chromium_selection = input("Enter your browser (chrome/thorium/vivaldi): ").lower()
        base_path = f"C:/Users/{user}/AppData/Local"
        if chromium_selection == 'chrome':
            base_path += "/Google Chrome/User Data/Default/Extensions/bkdgflcldnnnapblkhphbgpggdiikppg"
        elif chromium_selection == 'thorium':
            base_path += "/Thorium/User Data/Default/Extensions/bkdgflcldnnnapblkhphbgpggdiikppg"
        elif chromium_selection == 'vivaldi':
            base_path += "/Vivaldi/User Data/Default/Extensions/bkdgflcldnnnapblkhphbgpggdiikppg"
        else:
            print("ERROR: Invalid chromium selection.")
            return
    elif browser_selection == 'edge':
        base_path = f"C:/Users/{user}/AppData/Local/Microsoft Edge/User Data/Default/Extensions/caoacbimdbbljakfhgikoodekdnlcgpk"
    else:
        print("ERROR: Invalid browser selection.")
        return

    try:
        subfolder = os.listdir(base_path)[0]
        manifest_path = os.path.join(base_path, subfolder, 'manifest.json')
    except (FileNotFoundError, IndexError) as e:
        print("ERROR: Subfolder not found or no subfolder exists.\n")
        print(e)
        return

    if not os.path.exists(manifest_path):
        print("ERROR: Manifest file not found")
        return
    
    with open(manifest_path, 'r') as f:
        manifest_data = json.load(f)
    
    if "chrome_settings_overrides" in manifest_data:
        if "search_provider" in manifest_data["chrome_settings_overrides"]:
            if not manifest_data["chrome_settings_overrides"]["search_provider"].get("is_default", True):
                print("ERROR: Patch already applied, you're good to go.")
            else:
                manifest_data["chrome_settings_overrides"]["search_provider"]["is_default"] = False
                print("Manifest patched.")
        else:
            print("ERROR: No search provider found in chrome_settings_overrides.")
    else:
        print("ERROR: No chrome_settings_overrides found in manifest.")
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest_data, f, indent=4)

if __name__ == "__main__":
    main()
