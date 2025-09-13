import os
import glob
from datetime import datetime


def merge_analysis_files():
    """
    Merge all psychological analysis text files into a single master file.
    """
    # Directory containing the analysis files
    input_dir = os.path.join(os.getcwd(), "output", "psychological_analysis")

    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} doesn't exist!")
        return

    # Find all .txt files (excluding any existing master file)
    pattern = os.path.join(input_dir, "*.txt")
    files = glob.glob(pattern)

    # Remove master file from list if it exists
    master_file = os.path.join(input_dir, "psychological_analysis_master.txt")
    files = [f for f in files if f != master_file]

    if not files:
        print("No analysis files found to merge!")
        return

    # Sort files by modification time (or name)
    files.sort(key=lambda x: os.path.getmtime(x))

    print(f"Found {len(files)} files to merge...")

    # Create master file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(master_file, 'w', encoding='utf-8') as master:
        master.write(f"PSYCHOLOGICAL ANALYSIS MASTER FILE\n")
        master.write(f"Generated: {timestamp}\n")
        master.write(f"Total Entries: {len(files)}\n")
        master.write(f"{'=' * 80}\n\n")

        for i, file_path in enumerate(files, 1):
            filename = os.path.basename(file_path)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))

            master.write(f"{'=' * 80}\n")
            master.write(f"ENTRY #{i} - {filename}\n")
            master.write(f"Created: {file_mtime.strftime('%Y-%m-%d %H:%M:%S')}\n")
            master.write(f"{'=' * 80}\n\n")

            # Read and append file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    master.write(content)
            except Exception as e:
                master.write(f"ERROR READING FILE: {str(e)}")

            master.write(f"\n\n{'=' * 80}\n\n")

    print(f"Successfully merged {len(files)} files into: {master_file}")

    # Optionally, ask if user wants to delete original files
    response = input("Delete original files? (y/N): ").strip().lower()
    if response == 'y':
        for file_path in files:
            try:
                os.remove(file_path)
                print(f"Deleted: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


if __name__ == "__main__":
    merge_analysis_files()