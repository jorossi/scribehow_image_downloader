import re
import os
import requests
from urllib.parse import urlparse
import uuid
from datetime import datetime

class PharseData:
    """ Extract image URLs from a Markdown file. By using regular expressions."""
    def __init__(self, file_path):
        """Initialize the PharseData object with the path to the input file."""
        self.file_path = file_path
        self.image_urls = []
    def extract_urls(self):
        """Extract image URLs from the input file."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        self.image_urls = re.findall(r'!\[.*?\]\((https?://[^)]+)\)', content)
        
        if not self.image_urls:
            # Raise an exception if no image URLs are found in the input file.
            print("No image URLs found in the input file.")
            raise ValueError("No image URLs found in the input file.")
        else:
            print(f"Found {len(self.image_urls)} image URLs in the input file.")
        
        return self.image_urls
        
class DownloadImage:
    """Download an image from a URL and save it in the specified folder."""
    def __init__(self, save_folder):
        self.save_folder = save_folder

    def validate_output_folder(self):
        """Check if the output folder exists and create it if it doesn't."""
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
            print(f"Created folder: {self.save_folder}")
        else:
            print(f"Folder already exists: {self.save_folder}")

    def download_image(self, url):
        """Download an image from a URL and save it in the specified folder."""
        try:
            id = str(uuid.uuid4())[:4]
            time = datetime.now().strftime("%Y_%m_%d_%H_%M")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            filename = f"{time}_{id}.jpg"
            save_path = os.path.join(self.save_folder, filename)
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            
            print(f"Downloaded: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")


if __name__ == "__main__":
    images = PharseData('input.txt').extract_urls()
    output = DownloadImage('images')
    output.validate_output_folder()
    for x in images:
        output.download_image(x)
