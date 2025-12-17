import os
import shutil
import time
import logging
from datetime import datetime
import argparse
import sys

import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(filename='organizer.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def load_config(config_path='config.yaml'):
    """Loads the configuration from the specified path."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_destination_folder(file_extension, destinations):
    """Gets the destination folder for a given file extension."""
    for folder, extensions in destinations.items():
        if file_extension.lower() in extensions:
            return folder
    return None

def organize_file(file_path, source_folder, destinations, verbose=False, dry_run=False):
    """Organizes a single file."""
    if not os.path.isfile(file_path):
        return

    file_extension = os.path.splitext(file_path)[1]
    dest_folder_name = get_destination_folder(file_extension, destinations)

    if dest_folder_name:
        dest_folder_path = dest_folder_name
        if not os.path.isabs(dest_folder_name):
            dest_folder_path = os.path.join(source_folder, dest_folder_name)
        dest_folder_path = os.path.expanduser(dest_folder_path)

        if not dry_run:
            os.makedirs(dest_folder_path, exist_ok=True)

        file_name = os.path.basename(file_path)
        dest_file_path = os.path.join(dest_folder_path, file_name)

        if os.path.exists(dest_file_path):
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            base, ext = os.path.splitext(file_name)
            new_file_name = f"{base}_{timestamp}{ext}"
            new_dest_file_path = os.path.join(dest_folder_path, new_file_name)
            log_message = f"Duplicate file: '{file_name}'. Renaming to '{new_file_name}'. Moving to '{dest_folder_path}'."
            logging.info(log_message)
            if verbose or dry_run:
                print(f"{'[DRY RUN] ' if dry_run else ''}{log_message}")
            dest_file_path = new_dest_file_path
        else:
            log_message = f"Moving '{file_name}' to '{dest_folder_path}'."
            logging.info(log_message)
            if verbose or dry_run:
                print(f"{'[DRY RUN] ' if dry_run else ''}{log_message}")

        if not dry_run:
            try:
                shutil.move(file_path, dest_file_path)
                success_message = f"Successfully moved '{file_name}' to '{dest_folder_path}'."
                logging.info(success_message)
                if verbose:
                    print(success_message)
            except Exception as e:
                error_message = f"Error moving '{file_name}' to '{dest_folder_path}': {e}"
                logging.error(error_message)
                if verbose:
                    print(error_message, file=sys.stderr)

class FileOrganizerHandler(FileSystemEventHandler):
    def __init__(self, source_folder, destinations, verbose=False, dry_run=False):
        self.source_folder = source_folder
        self.destinations = destinations
        self.verbose = verbose
        self.dry_run = dry_run

    def on_created(self, event):
        organize_file(event.src_path, self.source_folder, self.destinations,
                      verbose=self.verbose, dry_run=self.dry_run)

def initial_scan(source_folder, destinations, verbose=False, dry_run=False):
    """Performs an initial scan of the source folder."""
    logging.info("Performing initial scan...")
    if verbose or dry_run:
        print(f"{'[DRY RUN] ' if dry_run else ''}Performing initial scan...")
    for item in os.listdir(source_folder):
        item_path = os.path.join(source_folder, item)
        organize_file(item_path, source_folder, destinations, verbose=verbose, dry_run=dry_run)
    logging.info("Initial scan complete.")
    if verbose or dry_run:
        print(f"{'[DRY RUN] ' if dry_run else ''}Initial scan complete.")

def main():
    """Main function to start the file organizer."""
    parser = argparse.ArgumentParser(description="Organize files automatically.")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Enable verbose output to console.")
    parser.add_argument('-c', '--config-file', default='config.yaml',
                        help="Path to the configuration file.")
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help="Perform a dry run without moving files.")
    parser.add_argument('-n', '--no-initial-scan', action='store_true',
                        help="Skip the initial scan of the source folder.")
    args = parser.parse_args()

    config = load_config(args.config_file)
    source_folder = os.path.expanduser(config['source_folder'])
    destinations = config['destinations']

    # Create source folder if it doesn't exist
    if not os.path.exists(source_folder):
        os.makedirs(source_folder)
        logging.info(f"Created source folder: {source_folder}")
        if args.verbose or args.dry_run:
            print(f"Created source folder: {source_folder}")


    if not args.no_initial_scan:
        initial_scan(source_folder, destinations, verbose=args.verbose, dry_run=args.dry_run)

    event_handler = FileOrganizerHandler(source_folder, destinations, verbose=args.verbose, dry_run=args.dry_run)
    observer = Observer()
    observer.schedule(event_handler, source_folder, recursive=False)
    observer.start()

    logging.info(f"Watching '{source_folder}' for new files...")
    if args.verbose or args.dry_run:
        print(f"Watching '{source_folder}' for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("File organizer stopped.")
        if args.verbose or args.dry_run:
            print("File organizer stopped.")
    observer.join()

if __name__ == "__main__":
    main()
