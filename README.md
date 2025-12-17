# Smart File Organizer

A Python-based tool to automatically organize files in a specified directory based on their extensions. It performs an initial scan to organize existing files and then monitors the directory for new files in real-time.

## Features

*   **Initial Scan**: On startup, the script scans the source folder and organizes all existing files according to the rules defined in `config.yaml`.
*   **Real-time Monitoring**: Uses the `watchdog` library to monitor the source folder for any new files and organizes them as they are created.
*   **Configurable**: Easily configure the source folder and destination mappings for different file types using the `config.yaml` file.
*   **Duplicate Handling**: If a file with the same name already exists in the destination folder, a timestamp is appended to the new file's name to prevent overwriting.
*   **Logging**: All file movement actions are logged to `organizer.log` for easy tracking.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/therealshammz/smart-file-organizer.git
    cd smart-file-organizer
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Configure the `config.yaml` file:**

    Open `config.yaml` and modify the `source_folder` and `destinations` to your liking. The `source_folder` is the directory you want to organize. The `destinations` can be simple names (which will be created inside the `source_folder`) or full, absolute paths (e.g., `/home/user/Documents`).

    Example `config.yaml`:
    ```yaml
    source_folder: '~/Downloads'
    destinations:
      '~/Pictures':
        - '.jpg'
        - '.png'
      '~/Documents':
        - '.pdf'
        - '.docx'
      Archives: # This will be created inside '~/Downloads'
        - '.zip'
    ```

2.  **Run the organizer script:**
    ```bash
    python3 organizer.py
    ```

    The script will perform an initial scan of the `source_folder` and then start monitoring for new files.

3.  **Stopping the script:**
    Press `Ctrl+C` in the terminal to stop the script.

## Command-line Arguments

You can use the following flags to control the script's behavior:

| Flag | Shorthand | Description |
|---|---|---|
| `--verbose` | `-v` | Prints detailed output of file movements to the console in real-time. |
| `--config-file <path>` | | Specifies the path to a configuration file. Defaults to `config.yaml`. |
| `--dry-run` | | Simulates the organization process without moving any files. Perfect for testing your configuration. |
| `--no-initial-scan` | | Skips the initial scan of the source folder and only monitors for new files. |

**Example:**

```bash
# Run a dry run with verbose output
python organizer.py --dry-run -v
```

## Log File

All actions are logged in `organizer.log`. This file contains information about which files were moved and where they were moved to. If any errors occur, they will also be logged here.
