import os
import pandas as pd
import requests
import random
import time
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def generate_dummy_photos(excel_file):
    photos_dir = "photos"
    
    # 1. Create directory
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)
        logging.info(f"Created folder: {photos_dir}")
    else:
        logging.info(f"Folder '{photos_dir}' already exists. New photos will be added here.")

    try:
        # 2. Read Roll Numbers from Excel
        logging.info("Reading Excel file to get Roll Numbers...")
        df = pd.read_excel(excel_file, sheet_name='in_roll_name_mapping')
        
        # specific to your file structure (Roll, Name)
        rolls = df['Roll'].unique()
        total = len(rolls)
        logging.info(f"Found {total} students. Starting download...")

        # 3. Download loop
        for i, roll in enumerate(rolls):
            roll = str(roll).strip()
            save_path = os.path.join(photos_dir, f"{roll}.jpg")

            # Skip if already exists (optional, remove check if you want to overwrite)
            if os.path.exists(save_path):
                # logging.info(f"Skipping {roll} (already exists)")
                continue

            # Generate a random human face URL
            # We use randomuser.me which provides free portrait placeholders
            gender = random.choice(['men', 'women'])
            img_id = random.randint(0, 99)
            url = f"https://randomuser.me/api/portraits/{gender}/{img_id}.jpg"

            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    print(f"[{i+1}/{total}] Downloaded photo for {roll}")
                else:
                    print(f"Failed to download for {roll}: Status {response.status_code}")
            
            except Exception as e:
                print(f"Error downloading {roll}: {e}")

            # Sleep briefly to be nice to the API
            time.sleep(0.1)

        logging.info("\n✅ Process Completed! You can now run the main allocation script.")

    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    file_name = input("Enter the input Excel file name (e.g., input.xlsx): ").strip()
    if os.path.exists(file_name):
        generate_dummy_photos(file_name)
    else:
        logging.error("File not found.")