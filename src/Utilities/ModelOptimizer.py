"""
Model optimization utilities for faster LLM inference
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

class ModelOptimizer:
    """Optimizes model loading and inference for better performance"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def loadOptimizedModel(self, modelName="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        """Load model with optimizations for faster inference"""
        try:
            print(f"Loading optimized model: {modelName}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(modelName)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with optimizations
            self.model = AutoModelForCausalLM.from_pretrained(
                modelName,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            # Optimize for inference
            self.model.eval()
            
            # Compile model for faster inference (PyTorch 2.0+)
            if hasattr(torch, 'compile'):
                try:
                    self.model = torch.compile(self.model)
                    print("Model compiled for faster inference")
                except Exception as e:
                    print(f"Model compilation failed: {e}")
            
            print("Optimized model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"Failed to load optimized model: {e}")
            return False
    
    def generateOptimized(self, prompt, maxTokens=50, temperature=0.1):
        """Generate text with optimizations"""
        if self.model is None or self.tokenizer is None:
            return None
        
        try:
            # Tokenize with truncation
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512,
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate with optimizations
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs.input_ids,
                    max_new_tokens=maxTokens,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    use_cache=True  # Enable KV cache for faster generation
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
            
        except Exception as e:
            print(f"Optimized generation failed: {e}")
            return None
    
    def getModelInfo(self):
        """Get information about the loaded model"""
        if self.model is None:
            return "No model loaded"
        
        totalParams = sum(p.numel() for p in self.model.parameters())
        trainableParams = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        return {
            "device": self.device,
            "totalParameters": totalParams,
            "trainableParameters": trainableParams,
            "modelDtype": next(self.model.parameters()).dtype
        }
