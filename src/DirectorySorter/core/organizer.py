import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Set
from shutil import move
from .config import OrganizerConfig

@dataclass
class OrganizationStats:
    """Statistics from organization run."""
    success: int = 0
    failed: int = 0
    skipped: int = 0
    errors: Dict[str, str] = field(default_factory=dict)

class Organizer:
    """Organizes files by extension with production-level error handling."""
    
    def __init__(self, config: OrganizerConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.stats = OrganizationStats()
        self._processed_extensions: Set[str] = set()
    
    def organize(self) -> OrganizationStats:
        """Run the organization process."""
        self.logger.info(f"Starting organization of {self.config.target_directory}")
        self.logger.debug(f"Dry run: {self.config.dry_run}")
        
        try:
            self._process_directory(self.config.target_directory)
            self.logger.info(f"Organization complete: {self.stats.success} moved, {self.stats.failed} failed")
        except Exception as e:
            self.logger.error(f"Fatal error during organization: {e}")
            raise
        
        return self.stats
    
    def _process_directory(self, directory: Path) -> None:
        """Process all files in directory."""
        for item in directory.iterdir():
            if item.is_file() and not self._should_skip(item):
                self._organize_file(item)
            elif item.is_dir() and self.config.recursive:
                self._process_directory(item)
    
    def _should_skip(self, file: Path) -> bool:
        """Check if file should be skipped."""
        for pattern in self.config.exclude_patterns:
            if file.match(pattern):
                self.logger.debug(f"Skipping {file}: matches pattern {pattern}")
                self.stats.skipped += 1
                return True
        return False
    
    def _organize_file(self, file: Path) -> None:
        """Move a single file to its destination."""
        ext = self._extract_extension(file)
        dest_dir = self.config.target_directory / ext
        try:
            self._create_directory(dest_dir, ext)
            dest_path = dest_dir / file.name
            self._move_file(file, dest_path)   
        except PermissionError as e:
            self._handle_error(file, "Permission denied", e)
        except Exception as e:
            self._handle_error(file, "Unexpected error", e)

    def _extract_extension(self, file: Path) -> str:
        """Extract the file extension, defaulting to 'Anonymous' if none."""
        return file.suffix[1:].lower() if file.suffix else "Anonymous"

    def _create_directory(self, dest_dir: Path, ext: str) -> None:
        # Create destination directory
        if not dest_dir.exists():
             if not self.config.dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Created directory: {dest_dir}")
                self._processed_extensions.add(ext)

    def _move_file(self, file: Path, dest_path: Path) -> None:
         # Move the file to the destination directory
         if not self.config.dry_run:
            move(str(file), str(dest_path))
            self.logger.debug(f"Moved {file} → {dest_path}")
         else:
           self.logger.debug(f"[DRY-RUN] Would move {file} → {dest_path}")            
           self.stats.success += 1           
        
    
    def _handle_error(self, file: Path, error_type: str, exception: Exception) -> None:
        """Handle file operation errors."""
        self.logger.error(f"{error_type} for {file}: {exception}")
        self.stats.failed += 1
        self.stats.errors[str(file)] = f"{error_type}: {str(exception)}"