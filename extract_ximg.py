import os
import zipfile

def verify_and_extract_ximg(archive_path, extract_to="extracted_workflows"):
    if not os.path.exists(archive_path):
        print(f"Error: Archive '{archive_path}' not found.")
        return False

    print(f"Verifying integrity of {archive_path}...")
    try:
        with zipfile.ZipFile(archive_path, 'r') as zf:
            # testzip() returns the name of the first bad file found, or None if all are intact
            bad_file = zf.testzip()
            if bad_file:
                print(f"Integrity check failed! Corrupted file found: {bad_file}")
                return False
            
            print("Archive integrity check passed successfully.")
            
            # Extract contents
            os.makedirs(extract_to, exist_ok=True)
            zf.extractall(extract_to)
            print(f"Successfully extracted archive contents to '{extract_to}/'")
            
            # List extracted files
            print("Contents:")
            for filename in zf.namelist():
                print(f"  - {filename}")
                
        return True
    except zipfile.BadZipFile:
        print("Error: The file is not a valid zip-based .ximg archive.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    verify_and_extract_ximg("oeneye_pages.ximg")

