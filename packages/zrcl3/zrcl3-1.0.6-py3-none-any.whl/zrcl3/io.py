import os
import shutil
import re
import glob

def _version_logic(bkup_path, bkup_name, file_ext, max_versions):
    """
    Handles the versioning logic for backups.
    Renames existing backups and returns the new backup name.
    """
    backup_pattern = os.path.join(bkup_path, f"{bkup_name}_v*{file_ext}")
    existing_backups = sorted(glob.glob(backup_pattern), reverse=True)

    # Rename existing backups with incremented version numbers
    for old_backup in existing_backups:
        version_match = re.search(r"_v(\d+)", old_backup)
        if version_match:
            old_version = int(version_match.group(1))
            new_version = old_version + 1
            if new_version <= max_versions:
                new_backup_name = re.sub(r"_v\d+", f"_v{new_version}", old_backup)
                os.rename(old_backup, new_backup_name)

    # Return the new backup name as v1
    return f"{bkup_name}_v1{file_ext}"

def create_bkup(path, bkup_path=None, max_versions=1, bkup_format="{name}.bak", delete_original=True):
    # Ensure the source file exists
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No file found at the specified path: {path}")

    # Determine the directory and file name
    dir_name, file_name = os.path.split(path)
    file_root, file_ext = os.path.splitext(file_name)

    # Set backup path
    if bkup_path is None:
        bkup_path = dir_name

    # Backup file name formatting
    bkup_name = bkup_format.format(name=file_root)

    # Handle versioning
    if max_versions > 1:
        bkup_name = _version_logic(bkup_path, bkup_name, file_ext, max_versions)
    else:
        bkup_name += file_ext

    # Create the backup
    shutil.copy2(path, os.path.join(bkup_path, bkup_name))
    if delete_original:
        os.remove(path)
        
        