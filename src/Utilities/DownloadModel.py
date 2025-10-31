import os
import urllib.request
import zipfile
from tqdm import tqdm
import subprocess
import sys

class ModelDownloader:
    
    def __init__(self):
        self.model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        self.model_name = "vosk-model-small-en-us-0.15"
        self.zip_filename = "model.zip"
        
        self.llmModelName = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.llmCacheDir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "transformers")
    
    def setupModelsDirectory(self):
        """Setup models directory"""
        modelsPath = "../models" 

        if not os.path.exists(modelsPath):
            os.makedirs(modelsPath)
            print(f"Created models directory at: {modelsPath}")
        
        return modelsPath
    
    def downloadWithProgress(self, url, filename):
        """Download file with progress bar"""
        def progressHook(blockNum, blockSize, totalSize):
            if totalSize > 0:
                pbar.update(blockSize)
        
        try:
            response = urllib.request.urlopen(url)
            totalSize = int(response.headers.get('Content-Length', 0))
            response.close()
        except:
            totalSize = 0
        
        # Download with progress bar
        with tqdm(total=totalSize, unit='B', unit_scale=True, desc="Downloading model") as pbar:
            urllib.request.urlretrieve(url, filename, progressHook)
        
        print(f"Downloaded {filename} successfully!")
    
    def extractModel(self, zipPath, extractTo):
        """Extract the model zip file"""
        print("Extracting model...")
        with zipfile.ZipFile(zipPath, 'r') as zipRef:
            fileList = zipRef.namelist()
            
            with tqdm(total=len(fileList), desc="Extracting files") as pbar:
                for file in fileList:
                    zipRef.extract(file, extractTo)
                    pbar.update(1)
        
        print("Model extracted successfully!")
    
    def downloadVoskModel(self):
        """Main method to download and setup Vosk model"""
        print("Setting up Vosk model...")
        
        modelsPath = self.setupModelsDirectory()
        modelPath = os.path.join(modelsPath, self.model_name)
        zipPath = os.path.join(modelsPath, self.zip_filename)
        
        if os.path.exists(modelPath):
            print(f"Model already exists at: {modelPath}")
            return modelPath
        
        try:
            self.downloadWithProgress(self.model_url, zipPath)
            
            self.extractModel(zipPath, modelsPath)
            
            os.remove(zipPath)
            print(f"Model ready at: {modelPath}")
            
            return modelPath
            
        except Exception as e:
            print(f"Error downloading model: {e}")
            # Clean up on error
            if os.path.exists(zipPath):
                os.remove(zipPath)
            return None

    def installLlmDependencies(self):
        """Install required dependencies for LLM functionality"""
        print("Installing LLM dependencies...")
        
        dependencies = [
            "torch",
            "transformers>=4.30.0", 
            "accelerate>=0.20.0",
            "sentencepiece"
        ]
        
        try:
            for dep in dependencies:
                print(f"Installing {dep}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", dep
                ])
            
            print(" LLM dependencies installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f" Failed to install LLM dependencies: {e}")
            return False
    
    def downloadLlmModel(self):
        """Download and setup the LLM model for autocorrect"""
        print("Setting up LLM model for autocorrect...")
        
        try:
            # Check if transformers is available
            import transformers
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            # First try to load from local cache only. If this fails then we'll download the model
            try:
                _ = AutoTokenizer.from_pretrained(self.llmModelName, local_files_only=True)
                model = AutoModelForCausalLM.from_pretrained(self.llmModelName, local_files_only=True)
                totalParams = sum(p.numel() for p in model.parameters())
                print("LLM model already cached. Skipping download.")
                print(f" Model parameters: {totalParams:,}")
                print(f" Model cache: {self.llmCacheDir}")
                return True
            except Exception:
                # Not in cache, proceed to download
                pass
            
            print(f"Downloading {self.llmModelName}...")
            
            # Download tokenizer
            print("Downloading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(self.llmModelName)
            
            # Download model
            print("Downloading model (this may take a while)...")
            model = AutoModelForCausalLM.from_pretrained(self.llmModelName)
            
            # Get model info
            totalParams = sum(p.numel() for p in model.parameters())
            print(f" LLM model downloaded successfully!")
            print(f" Model parameters: {totalParams:,}")
            print(f" Model cached at: {self.llmCacheDir}")
            
            return True
            
        except ImportError:
            print(" Transformers library not found. Installing dependencies first...")
            if self.installLlmDependencies():
                return self.downloadLlmModel()  # Retry after installation
            else:
                return False
                
        except Exception as e:
            print(f" Failed to download LLM model: {e}")
            return False
    
    def checkLlmAvailability(self):
        """Check if LLM model is available and working"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            # Try to load the model
            tokenizer = AutoTokenizer.from_pretrained(self.llmModelName, local_files_only=True)
            model = AutoModelForCausalLM.from_pretrained(self.llmModelName, local_files_only=True)
            
            print("✅ LLM model is available and working!")
            return True
            
        except Exception as e:
            print(f" LLM model not available: {e}")
            return False
    
    def setupAllModels(self):
        """Setup both Vosk and LLM models"""
        print(" Setting up all models...")
        print("=" * 50)
        
        # Setup Vosk model
        voskSuccess = self.downloadVoskModel()
        
        # Setup LLM model
        llmSuccess = self.downloadLlmModel()
        
        print("\n Setup Summary:")
        print(f"Vosk Model: {' Ready' if voskSuccess else ' Failed'}")
        print(f"LLM Model: {' Ready' if llmSuccess else ' Failed'}")
        
        if voskSuccess and llmSuccess:
            print("All models ready! Autocorrect with LLM is available.")
        elif voskSuccess:
            print("Vosk ready, but LLM failed. Autocorrect will use fallback mode.")
        else:
            print("❌ Model setup failed.")
        
        return voskSuccess, llmSuccess

    def routineSetupModel(self):
        downloader = ModelDownloader()
        modelPath = downloader.downloadVoskModel()
    
        if modelPath:
            print(f"✅ Vosk model setup complete!")
            print(f"📁 Model location: {modelPath}")
        else:
            print("❌ Failed to download model")