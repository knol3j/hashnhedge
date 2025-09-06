"""File handling utilities."""
import hashlib
from pathlib import Path

class FileHelper:
    """File operations helper."""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
    
    def ensure_dir(self, path):
        """Ensure directory exists."""
        Path(path).mkdir(parents=True, exist_ok=True)
        return Path(path)
    
    def get_file_hash(self, file_path):
        """Get SHA-256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
