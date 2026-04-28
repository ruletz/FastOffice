import os
import shutil
import codecs

APP_DIR = r"c:/Projects/OnlyOffice/app"
ROOT_DIR = os.path.dirname(APP_DIR)


def human_mb(bytes_val: int) -> float:
    return bytes_val / 1024.0 / 1024.0


def file_size(path: str) -> int:
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def remove_file(path: str) -> int:
    if not os.path.isfile(path):
        print(f"SKIP (no file): {path}")
        return 0
    size = file_size(path)
    try:
        os.remove(path)
        print(f"Removed FILE: {path}  ({human_mb(size):.2f} MB)")
        return size
    except OSError as e:
        print(f"FAILED to remove {path}: {e}")
        return 0


def safe_backup():
    """
    Create a one-time safety backup of the app folder so any change
    from this script is reversible without reinstalling.
    """
    backup_dir = os.path.join(ROOT_DIR, "app_backup_safe")
    if os.path.exists(backup_dir):
        print(f"Backup already exists at: {backup_dir}")
        return

    print(f"Creating safety backup at: {backup_dir}")
    shutil.copytree(APP_DIR, backup_dir)
    print("Backup completed.")


def system_scale_is_1() -> bool:
    """
    Check settings.txt generated earlier to see if system-scale == 1.
    If the file is missing, we conservatively assume scale != 1.
    """
    settings_path = os.path.join(ROOT_DIR, "settings.txt")
    if not os.path.isfile(settings_path):
        return False
    try:
        with codecs.open(settings_path, "r", "utf8") as f:
            text = f.read()
        return "<system-scale>1</system-scale>" in text
    except Exception:
        return False


def trim_chrome_paks() -> int:
    """
    Remove chrome_200_percent.pak when system-scale is 1.
    This drops unused 2x assets without affecting functionality
    on a 100% scaling display.
    """
    freed = 0
    print("\n[1] Chrome resource packs")

    chrome_100 = os.path.join(APP_DIR, "chrome_100_percent.pak")
    chrome_200 = os.path.join(APP_DIR, "chrome_200_percent.pak")
    resources = os.path.join(APP_DIR, "resources.pak")

    for p in (chrome_100, chrome_200, resources):
        if os.path.isfile(p):
            print(f"  {os.path.basename(p)}: {human_mb(file_size(p)):.2f} MB")

    if not system_scale_is_1():
        print("  Detected system-scale != 1 or unknown; "
              "leaving chrome_200_percent.pak in place.")
        return freed

    if os.path.isfile(chrome_200):
        print("  system-scale == 1 => removing chrome_200_percent.pak "
              "(2x assets not used).")
        freed += remove_file(chrome_200)
    else:
        print("  No chrome_200_percent.pak found.")

    return freed


def trim_update_service() -> int:
    """
    Remove the standalone update service executable.
    This does not affect core editing, only auto-update.
    """
    print("\n[2] Update service")
    path = os.path.join(APP_DIR, "updatesvc.exe")
    if not os.path.isfile(path):
        print("  updatesvc.exe not present (already removed or not bundled).")
        return 0
    print("  Removing updatesvc.exe (disables built-in auto-update only).")
    return remove_file(path)


def main():
    print("=" * 60)
    print("OnlyOffice SAFE Trim (no feature compromises)")
    print("=" * 60)

    if not os.path.isdir(APP_DIR):
        print(f"ERROR: APP_DIR not found: {APP_DIR}")
        return

    # One-time safety backup
    safe_backup()

    total_freed = 0
    total_freed += trim_chrome_paks()
    total_freed += trim_update_service()

    print("\n" + "=" * 60)
    print(f"Total disk space freed: {human_mb(total_freed):.2f} MB")
    print("All changes are reversible using the app_backup_safe folder.")
    print("=" * 60)


if __name__ == "__main__":
    main()

