import os
import urllib.request
import zipfile
from tqdm import tqdm

class ModelDownloader:
    
    def __init__(self):
        self.model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        self.model_name = "vosk-model-small-en-us-0.15"
        self.zip_filename = "model.zip"
    
    def setup_models_directory(self):
        """Setup models directory"""
        models_path = "../models"  # From src/ directory, go up one level to project root, then into models

        if not os.path.exists(models_path):
            os.makedirs(models_path)
            print(f"Created models directory at: {models_path}")
        
        return models_path
    
    def download_with_progress(self, url, filename):
        """Download file with progress bar"""
        def progress_hook(block_num, block_size, total_size):
            if total_size > 0:
                pbar.update(block_size)
        
        try:
            response = urllib.request.urlopen(url)
            total_size = int(response.headers.get('Content-Length', 0))
            response.close()
        except:
            total_size = 0
        
        # Download with progress bar
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading model") as pbar:
            urllib.request.urlretrieve(url, filename, progress_hook)
        
        print(f"Downloaded {filename} successfully!")
    
    def extract_model(self, zip_path, extract_to):
        """Extract the model zip file"""
        print("Extracting model...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            
            with tqdm(total=len(file_list), desc="Extracting files") as pbar:
                for file in file_list:
                    zip_ref.extract(file, extract_to)
                    pbar.update(1)
        
        print("Model extracted successfully!")
    
    def download_vosk_model(self):
        """Main method to download and setup Vosk model"""
        print("Setting up Vosk model...")
        
        models_path = self.setup_models_directory()
        model_path = os.path.join(models_path, self.model_name)
        zip_path = os.path.join(models_path, self.zip_filename)
        
        if os.path.exists(model_path):
            print(f"Model already exists at: {model_path}")
            return model_path
        
        try:
            self.download_with_progress(self.model_url, zip_path)
            
            self.extract_model(zip_path, models_path)
            
            os.remove(zip_path)
            print(f"Model ready at: {model_path}")
            
            return model_path
            
        except Exception as e:
            print(f"Error downloading model: {e}")
            # Clean up on error
            if os.path.exists(zip_path):
                os.remove(zip_path)
            return None

    def routineSetupModel(self):
        downloader = ModelDownloader()
        model_path = downloader.download_vosk_model()
    
        if model_path:
            print(f"✅ Vosk model setup complete!")
            print(f"📁 Model location: {model_path}")
        else:
            print("❌ Failed to download model")