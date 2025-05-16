
# :: Finds repository root by traversing upward until finding a marker file or directory

import os
import pathlib


def get_repo_root():
    # Traverse upward until we find the marker (.env) that indicates the repo root
    current_dir = pathlib.Path(os.getcwd())
    while current_dir != current_dir.parent:  # Stop at filesystem root
        if (current_dir / '.env').exists() or (current_dir / '.gitignore').exists():
            return current_dir
        current_dir = current_dir.parent

    raise FileNotFoundError("Could not locate repository root. Make sure you're running from within the repository.")
