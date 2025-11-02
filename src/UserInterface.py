import tkinter as tk
from tkinter import ttk


class UserInterface:
    """Main user interface window for PocketAlexa"""
    
    def __init__(self, executor, interpreter, autocorrect, file_logger, app_registry=None):
        """
        Initialize the UserInterface with access to core components.
        
        Args:
            executor: Executor instance for command execution
            interpreter: Interpreter instance for speech parsing
            autocorrect: Autocorrect instance for command correction
            file_logger: FileLogger instance for logging
            app_registry: ApplicationRegistry instance (optional, defaults to autocorrect's registry)
        """
        # Store references to core components
        self.executor = executor
        self.interpreter = interpreter
        self.autocorrect = autocorrect
        self.file_logger = file_logger
        self.app_registry = app_registry or autocorrect.appRegistry
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("PocketAlexa")
        self.root.geometry("800x600")
        
        # Setup UI components
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize and configure UI widgets"""
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Placeholder for future widgets
        # Additional ttk widgets can be added here later
        
    def run(self):
        """Start the UI mainloop"""
        self.root.mainloop()
    
    def close(self):
        """Close the UI window"""
        self.root.destroy()

