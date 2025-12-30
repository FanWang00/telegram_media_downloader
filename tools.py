from pathlib import Path

def read_missing_names(root: str = "", out_file: str = "missing_names.txt") -> list:
    """
    Reads the missing names from the specified file and returns them as a list of strings.
    
    Parameters:
        root (str): The directory path where the file is located.
        out_file (str): The name of the file to read. Default is "missing_names.txt".
        
    Returns:
        list: A list of missing names.
    """
    out_path = Path(root) / out_file

    try:
        with open(out_path, "r", encoding="utf-8") as f:
            missing_lines = f.readlines()

        # Clean the lines, remove extra newlines or spaces
        missing_names = [line.strip() for line in missing_lines]

        return missing_names

    except FileNotFoundError:
        print(f"File not found: {out_path}")
        return []

