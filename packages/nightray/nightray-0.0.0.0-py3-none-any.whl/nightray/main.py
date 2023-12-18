import argparse
import os

def list_files_in_directory(path="."):
    """
    List files and directories in the specified path.

    Parameters:
    - path (str): The path to the directory. Defaults to the current directory.
    """
    try:
        # Get the list of files and directories in the specified path
        file_list = os.listdir(path)

        # Print the list
        print(f"Files and directories in '{path}':")
        for item in file_list:
            print(item)

    except FileNotFoundError:
        print(f"Error: The specified path '{path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied for '{path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def search_keyword_in_files(path=".", keyword=""):
    """
    Recursively search for a keyword within files in the specified path and its subdirectories.

    Parameters:
    - path (str): The path to the directory. Defaults to the current directory.
    - keyword (str): The keyword to search for in the files.
    """
    try:
        # Initialize a list to store matching file paths
        matching_files = []

        # Walk through the directory and its subdirectories
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)

                # Search for the keyword in each file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        contents = f.read()
                        if keyword in contents:
                            matching_files.append(file_path)
                except UnicodeDecodeError:
                    print(f"Error: Unable to decode file '{file_path}'.")

        # Print the list of matching files
        if matching_files:
            print(f"Files containing the keyword '{keyword}':")
            for file_path in matching_files:
                print(file_path)
        else:
            print(f"No files found containing the keyword '{keyword}'.")

    except FileNotFoundError:
        print(f"Error: The specified path '{path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied for '{path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="nightray - A simple command-line tool")

    # Add arguments
    parser.add_argument("command", choices=["list", "search"], help="Command to execute")
    parser.add_argument("--path", default=".", help="The path to the directory (default: current directory)")
    parser.add_argument("--keyword", help="The keyword to search for (required for 'search' command)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Execute the specified command
    if args.command == "list":
        list_files_in_directory(args.path)
    elif args.command == "search":
        if not args.keyword:
            parser.error("The '--keyword' argument is required for the 'search' command.")
        search_keyword_in_files(args.path, args.keyword)
    else:
        parser.error("Invalid command. Use 'list' or 'search'.")

if __name__ == "__main__":
    main()