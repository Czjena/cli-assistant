import os

def list_files_in_cwd():
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    print("Files and directories in current folder:")
    for entry in os.listdir(cwd):
        print(f" - {entry}")