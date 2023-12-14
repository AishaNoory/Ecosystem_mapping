import os

# Define the root directory where the subdirectories are located
root_directory = r'C:\Users\busta\OneDrive\Desktop\stakeholder_mapping\Data_extracted\GNR_PDD\Goldstd_unverified'

# Iterate through each folder in the root directory
for folder in os.listdir(root_directory):
    # Construct the full path of the current folder
    folder_path = os.path.join(root_directory, folder)

    # Check if the current item is a directory
    if os.path.isdir(folder_path):
        # Iterate through each file in the subdirectory
        for filename in os.listdir(folder_path):
            # Check if the current file is 'default_vector_store.json'
            if filename == 'default_vector_store.json':
                # Construct the full path of the file to be renamed
                old_file_path = os.path.join(folder_path, filename)

                # Construct the new file name and its full path
                new_file_path = os.path.join(folder_path, 'vector_store.json')

                # Rename the file
                os.rename(old_file_path, new_file_path)

# The script is now complete.
