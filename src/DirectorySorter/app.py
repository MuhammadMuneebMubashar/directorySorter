from .core import Organizer

class App:
    """
    Main application layer for the file-organizing program.

    The App class creates an Organizer, starts the organizing process,
    and displays the final results.
    """

    def __init__(self, directory_path: str) -> None:
        """
        Initialize the application.

        Args:
            directory_path (str): Path of the directory to organize.
        """
        self.organizer = Organizer(directory_path)

    def run(self) -> None:
        """
        Start the organizing process and display the results.

        The actual file organization is delegated to the Organizer
        instance.
        """
        self.organizer.organize_folder()

        print(f"Files moved successfully: {self.organizer.stats['success']}")
        print(f"Files failed to move: {self.organizer.stats['fail']}")

