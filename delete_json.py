import os

root_directory = r"C:\Users\user\Downloads\stakeholder_mapping\stakeholder_mapping\Data_extracted\GNR_PDD\verra_verified\verra_verified"

def delete_json_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

delete_json_files(root_directory)
