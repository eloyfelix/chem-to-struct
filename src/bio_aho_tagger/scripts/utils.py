import requests
import os

def download_file(url, filename):
    """Download the file if it does not already exist."""
    # Check if the file already exists
    if os.path.exists(filename):
        print(f"The file '{filename}' already exists. Skipping download.")
        return

    print(f"Downloading file from {url}...")
    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File downloaded successfully: {filename}")
        else:
            raise Exception(
                f"Failed to download the file. Status code: {response.status_code}"
            )
