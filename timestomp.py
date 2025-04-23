import os
import datetime
import platform
import sys

def change_all_timestamps():
    """Modify creation, modification, and access timestamps of a file"""
    
    print("\n=== File Time Machine ===")
    print("Change ALL timestamps (created, modified, accessed)\n")
    
    # Get file path
    while True:
        file_path = input("Drag file here or type path: ").strip('"\' ')
        if os.path.exists(file_path):
            break
        print(f"✖ Error: File '{file_path}' not found")

    # Show original timestamps
    print("\nCURRENT TIMESTAMPS:")
    if platform.system() == 'Windows':
        show_windows_timestamps(file_path)
    else:
        show_unix_timestamps(file_path)

    # Get time adjustment
    print("\nHow far back should we go?")
    days = int(input("Days: ") or 0)
    hours = int(input("Hours: ") or 0)
    minutes = int(input("Minutes: ") or 0)
    seconds = int(input("Seconds: ") or 0)
    time_shift = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    # Apply changes
    if input("\nConfirm change? (y/n): ").lower() == 'y':
        if platform.system() == 'Windows':
            change_windows_timestamps(file_path, time_shift)
        else:
            change_unix_timestamps(file_path, time_shift)
        print("\n✔ Success! Check file properties.")
    else:
        print("\nNo changes made.")

def show_windows_timestamps(file_path):
    """Display Windows timestamps"""
    try:
        import win32file
        handle = win32file.CreateFile(
            file_path, win32file.GENERIC_READ,
            0, None, win32file.OPEN_EXISTING, 0, None)
        ctime, atime, mtime = win32file.GetFileTime(handle)
        handle.close()
        
        print(f"Created:  {convert_windows_time(ctime)}")
        print(f"Modified: {convert_windows_time(mtime)}")
        print(f"Accessed: {convert_windows_time(atime)}")
    except ImportError:
        print("(Install pywin32 to see creation time)")
        stat = os.stat(file_path)
        print(f"Modified: {datetime.datetime.fromtimestamp(stat.st_mtime)}")
        print(f"Accessed: {datetime.datetime.fromtimestamp(stat.st_atime)}")

def change_windows_timestamps(file_path, time_shift):
    """Modify Windows timestamps"""
    try:
        import win32file
        import pywintypes
        
        # Get current times
        handle = win32file.CreateFile(
            file_path, win32file.GENERIC_READ,
            0, None, win32file.OPEN_EXISTING, 0, None)
        ctime, atime, mtime = win32file.GetFileTime(handle)
        handle.close()
        
        # Calculate new times
        new_ctime = convert_windows_time(ctime) - time_shift
        new_atime = convert_windows_time(atime) - time_shift
        new_mtime = convert_windows_time(mtime) - time_shift
        
        # Apply changes
        handle = win32file.CreateFile(
            file_path, win32file.GENERIC_WRITE,
            0, None, win32file.OPEN_EXISTING, 0, None)
        win32file.SetFileTime(
            handle,
            pywintypes.Time(new_ctime.timestamp()),
            pywintypes.Time(new_atime.timestamp()),
            pywintypes.Time(new_mtime.timestamp()))
        handle.close()
        
    except ImportError:
        print("⚠ Using basic timestamp change (install pywin32 for creation time)")
        stat = os.stat(file_path)
        new_atime = datetime.datetime.fromtimestamp(stat.st_atime) - time_shift
        new_mtime = datetime.datetime.fromtimestamp(stat.st_mtime) - time_shift
        os.utime(file_path, (new_atime.timestamp(), new_mtime.timestamp()))

def show_unix_timestamps(file_path):
    """Display Unix timestamps"""
    stat = os.stat(file_path)
    print(f"Modified: {datetime.datetime.fromtimestamp(stat.st_mtime)}")
    print(f"Accessed: {datetime.datetime.fromtimestamp(stat.st_atime)}")
    print(f"Changed:  {datetime.datetime.fromtimestamp(stat.st_ctime)} (metadata change)")

def change_unix_timestamps(file_path, time_shift):
    """Modify Unix timestamps"""
    stat = os.stat(file_path)
    new_atime = datetime.datetime.fromtimestamp(stat.st_atime) - time_shift
    new_mtime = datetime.datetime.fromtimestamp(stat.st_mtime) - time_shift
    os.utime(file_path, (new_atime.timestamp(), new_mtime.timestamp()))

def convert_windows_time(windows_time):
    """Convert Windows FILETIME to datetime"""
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=windows_time//10)

if __name__ == "__main__":
    change_all_timestamps()
    input("\nPress Enter to exit...")