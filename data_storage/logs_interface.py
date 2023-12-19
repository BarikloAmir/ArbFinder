from datetime import datetime


def save_errors_to_log_file(error_message: str):
    """Save errors to the log file."""
    log_file_path = 'error_log.txt'  # Specify the path to your log file

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Use the 'with' statement to ensure proper file handling (auto-closes the file)
    with open(log_file_path, 'a') as log_file:
        # 'a' mode appends to the file, creating it if it doesn't exist
        log_file.write(f"{timestamp} - {error_message}\n")