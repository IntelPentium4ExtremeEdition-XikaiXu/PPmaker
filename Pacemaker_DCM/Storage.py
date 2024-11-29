import json
import os

class FileIO:
    """Class for handling file operations such as reading and writing JSON files."""

    def __init__(self, fileName):
        """Initialize with a file name."""
        self.__fileName = fileName

    def writeText(self, text):
        """Write a dictionary to a JSON file. Create the file if it doesn't exist."""
        data = self.readText() or {}
        data.update(text)
        with open(self.__fileName, "w") as f:
            json.dump(data, f)

    def readText(self):
        """Read and return the contents of a JSON file as a dictionary."""
        if os.path.isfile(self.__fileName):
            try:
                with open(self.__fileName, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from {self.__fileName}.")
        return None

    def getFileName(self):
        """Return the file name."""
        return self.__fileName

    def getlength(self):
        """Return the number of keys in the JSON file."""
        data = self.readText()
        return len(data) if data else 0


