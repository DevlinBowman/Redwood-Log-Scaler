import os


# Define the directory and necessary files
def initialize_live_dir():
    print("Initializing Live/ directory and necessary files")
    live_directory = "Live/"
    necessary_files = ["user_supplied_input.txt",
                       "formatted_user_supplied_input.txt"]

# Function to ensure directory exists

    def ensure_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

# Function to ensure file exists

    def ensure_file(file_path):
        if not os.path.isfile(file_path):
            # Create the file if it does not exist
            open(file_path, 'a').close()


# Ensure the Live/ directory exists
    ensure_directory(live_directory)

# Ensure all necessary files exist within the Live/ directory
    for file_name in necessary_files:
        file_path = os.path.join(live_directory, file_name)
        ensure_file(file_path)
