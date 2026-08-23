from dataclasses import dataclass, field
from pathlib import Path
from typing import set

@dataclass
class OrganizerConfig:
    """Configuration for the file organizer."""
    
    target_directory: Path
    dry_run: bool = False
    recursive: bool = False
    group_strategy: str = "extension"  # or "type", "date", etc.
    exclude_patterns:set[str] = field(default_factory=set)
    log_level: str = "INFO"
    
    def __post_init__(self):
        """Validate config after initialization."""
        self.target_directory = Path(self.target_directory)
        if not self.target_directory.exists():
            raise FileNotFoundError(f"Directory {self.target_directory} does not exist")
        if not self.target_directory.is_dir():
            raise NotADirectoryError(f"{self.target_directory} is not a directory")