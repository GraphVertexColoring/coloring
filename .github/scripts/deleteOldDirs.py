import os
import shutil
import time

# Directories to clean up
TARGET_DIRS = ["analysis", "docs"]
RETENTION_DAYS = 100  # Number of days before deletion (2 weeks)
CURRENT_TIME = time.time()
EXCLUSION_DIRS = ["_layouts", "assets", "example"]

def delete_old_subdirectories(directory, retention_days):
    if not os.path.exists(directory) or not os.path.isdir(directory):
        print(f"Skipping {directory}: Not a valid directory")
        return

    # Iterate through subdirectories
    for subdir in os.listdir(directory):
        subdir_path = os.path.join(directory, subdir)
        if os.path.isdir(subdir_path) and subdir_path not in EXCLUSION_DIRS:
            # Get last modification time
            last_modified = os.path.getmtime(subdir_path)
            age_days = (CURRENT_TIME - last_modified) / 86400  # Convert seconds to days

            # Delete if older than retention_days
            if age_days > retention_days:
                print(f"Deleting {subdir_path} (Age: {int(age_days)} days)")
                shutil.rmtree(subdir_path)

# Run cleanup for each target directory
for target in TARGET_DIRS:
    delete_old_subdirectories(target, RETENTION_DAYS)