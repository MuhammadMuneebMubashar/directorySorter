"""
File Organizer

This module provides a simple file-organizing application that groups files
inside a specified directory into subdirectories based on their file
extensions.

For example:

    sorting_practice/
        photo.jpg
        document.pdf
        song.mp3

will be organized into:

    sorting_practice/
        jpg/
            photo.jpg
        pdf/
            document.pdf
        mp3/
            song.mp3

The module contains two main classes:

    Organizer:
        Contains the core file-organizing logic.

    App:
        Acts as the application layer responsible for starting the organizer
        and displaying the final results.
"""

from pathlib import Path
import shutil


class Organizer:
    """
    Organizes files in a directory according to their file extensions.

    The Organizer class is responsible for:
        - Validating the provided directory path.
        - Inspecting files inside the directory.
        - Extracting file extensions.
        - Creating extension-based directories.
        - Moving files into their corresponding directories.
        - Tracking successful and failed file movements.
    """

    def __init__(self, directoryPath: str) -> None:
        """
        Initialize an Organizer for the specified directory.

        Args:
            directoryPath (str): Path of the directory to organize.

        Raises:
            FileNotFoundError: If the specified path does not exist.
            NotADirectoryError: If the specified path is not a directory.
        """
        self.directoryPath = self.__form_Path(directoryPath)
        self.extensions = []
        self.stats = dict(success=0, fail=0)

    def __form_Path(self, path: str) -> Path:
        """
        Validate the provided path and convert it into a Path object.

        The method checks that the path exists and that it represents
        a directory.

        Args:
            path (str): Path to validate.

        Returns:
            Path: Validated directory path.

        Raises:
            FileNotFoundError: If the path does not exist.
            NotADirectoryError: If the path is not a directory.
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"The path {path} does not exist.")

        if not path.is_dir():
            raise NotADirectoryError(f"The path {path} is not a directory.")

        return path

    def organize_folder(self) -> None:
        """
        Organize files in the target directory by their extensions.

        Each file is inspected to determine its extension. A directory
        corresponding to that extension is created if necessary, and
        the file is then moved into that directory.

        Files without an extension are ignored.
        """
        for file in self.directoryPath.iterdir():
            ext = self.__extract_extension(file)

            if ext:
                directory_exists, directory_path = self.__get_directory_path(ext)

                if not directory_exists:
                    self.extensions.append(ext)
                    self.__create_directory(directory_path)

                file_path = self.__get_file_path(file)
                self.__move_file(file_path, directory_path)

    def __extract_extension(self, file: Path) -> str | None:
        """
        Extract the extension from a file.

        Directories are ignored because only actual files have their
        extensions extracted.

        Args:
            file (Path): File or directory to inspect.

        Returns:
            str | None:
                The file extension without the leading dot.
                Returns None if the path is not a file.
        """
        if file.is_file():
            return file.suffix[1:]

        return None

    def __get_directory_path(self, ext: str) -> tuple[bool, Path]:
        """
        Determine the directory path associated with a file extension.

        The extension directory is located inside the target directory.

        For example, if the extension is 'pdf', the resulting path will be:

            target_directory/pdf

        Args:
            ext (str): File extension.

        Returns:
            tuple[bool, Path]:
                The first value indicates whether the directory already
                exists or has already been registered.

                The second value is the Path object for that directory.
        """
        directory_path = self.directoryPath / ext

        if ext in self.extensions or (directory_path).exists():
            return True, directory_path

        return False, directory_path

    def __get_file_path(self, file: Path) -> Path:
        """
        Construct the complete path of a file inside the target directory.

        Args:
            file (Path): File whose path is required.

        Returns:
            Path: Complete path to the file.
        """
        return self.directoryPath / file.name

    def __create_directory(self, directory_path: Path):
        """
        Create the directory for a particular file extension.

        The directory and any required parent directories are created.
        Permission and operating-system errors are caught and displayed.

        Args:
            directory_path (Path): Directory that should be created.
        """
        try:
            directory_path.mkdir(parents=True, exist_ok=True)

        except PermissionError as e:
            print(f"Permission denied: {e}")

        except OSError as e:
            print(f"OS error: {e}")

    def __move_file(self, file_path: Path, directory_path: Path) -> None:
        """
        Move a file to its corresponding extension directory.

        If the operation succeeds, the success counter is incremented.
        If a permission or operating-system error occurs, the failure
        counter is incremented.

        Args:
            file_path (Path): Path of the file to move.
            directory_path (Path): Destination directory.
        """
        try:
            shutil.move(file_path, directory_path)

            self.stats['success'] += 1
            return

        except PermissionError as e:
            print(f"Permission denied: {e}")

        except OSError as e:
            print(f"OS error: {e}")

        self.stats['fail'] += 1

