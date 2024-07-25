"""

BLUEPRINT TO UNDERSTAND IT BETTER
LLD FILE SYSTEM SEARCH

Classes:
1. File: Represents a file in the file system.
   - Attributes: name, extension, size
   - Methods: get_name(), get_extension(), get_size()

2. FileSystem: Represents a directory or a collection of files.
   - Attributes: name, is_directory, sub_directories, files
   - Methods: None

3. Filter (Abstract Class): Base class for different types of file filters.
   - Methods: match(file) -> bool

4. NameFilter: Filters files based on their name.
   - Inherits: Filter
   - Attributes: name
   - Methods: match(file) -> bool

5. SizeFilter: Filters files based on their size with a given comparison operator.
   - Inherits: Filter
   - Attributes: size, operator
   - Methods: match(file) -> bool

6. ExtensionFilter: Filters files based on their extension.
   - Inherits: Filter
   - Attributes: extension
   - Methods: match(file) -> bool

7. Search: Handles searching files in the file system based on provided filters.
   - Attributes: file_system, filters, condition
   - Methods: check_conditions(file) -> bool, find_files() -> List[str]

Usage:
- Initialize FileSystem with directories and files.
- Create specific filter objects (NameFilter, SizeFilter, ExtensionFilter).
- Create a Search object with the FileSystem and a list of filters.
- Call find_files() method to get a list of files that match the filters.


"""
from abc import ABC, abstractmethod
from typing import List

class File:
    def __init__(self, name: str, extension: str, size: int):
        self.name = name
        self.extension = extension
        self.size = size

class Directory:
    def __init__(self, name: str, is_directory: bool = False):
        self.name = name
        self.is_directory = is_directory
        self.subdirectories = []
        self.files = []

class Filter(ABC):
    @abstractmethod
    def match(self, file: File) -> bool:
        pass

class NameFilter(Filter):
    def __init__(self, name: str):
        self.name = name

    def match(self, file: File) -> bool:
        return file.name == self.name

class SizeFilter(Filter):
    def __init__(self, size: int, operator: str):
        self.size = size
        self.operator = operator

    def match(self, file: File) -> bool:
        return eval(f"{file.size} {self.operator} {self.size}")

class ExtensionFilter(Filter):
    def __init__(self, extension: str):
        self.extension = extension

    def match(self, file: File) -> bool:
        return file.extension == self.extension

class FileSearch:
    def __init__(self, root_directory: Directory, filters: List[Filter], condition: str = "AND"):
        self.root_directory = root_directory
        self.filters = filters
        self.condition = condition

    def check_conditions(self, file: File) -> bool:
        if self.condition == "AND":
            for f in self.filters:
                if not f.match(file):
                    return False
            return True
        elif self.condition == "OR":
            for f in self.filters:
                if f.match(file):
                    return True
            return False
        return False

    def find_files(self) -> List[str]:
        queue = [self.root_directory]
        result = []

        while queue:
            current_directory = queue.pop(0)
            for file in current_directory.files:
                if self.check_conditions(file):
                    result.append(file.name)
            queue.extend(current_directory.subdirectories)

        return result
    

if __name__ == "__main__":
    # Simulation
    f1 = File("abc", "txt", 10)
    f2 = File("cde", "txt", 20)
    f3 = File("def", "pdf", 30)
    f4 = File("ghi", "py", 5)
    f5 = File("uvw", "java", 10)

    root_directory = Directory("/", True)
    root_directory.files = [f1, f2, f3, f4, f5]

    # Example searches
    res = FileSearch(root_directory, [NameFilter("abc")]).find_files()
    print("Files with name 'abc':", res)

    res = FileSearch(root_directory, [SizeFilter(10, ">=")]).find_files()
    print("Files with size >= 10:", res)

    res = FileSearch(root_directory, [ExtensionFilter("java"), SizeFilter(10, ">=")], "OR").find_files()
    print("Files with extension 'java' OR size >= 10:", res)

