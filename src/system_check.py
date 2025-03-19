import sys

def check_system():
    if sys.platform == 'darwin':
        return 'macOS'
    else:
        return 'win'

if __name__ == "__main__":
    check_system()