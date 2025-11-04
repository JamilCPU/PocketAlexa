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
        self.executor = executor
        self.interpreter = interpreter
        self.autocorrect = autocorrect
        self.file_logger = file_logger
        self.app_registry = app_registry or autocorrect.appRegistry
        
        self.root = tk.Tk()
        self.root.title("PocketAlexa")
        self.root.geometry("800x600")
        
        self.style = ttk.Style(self.root)
        self.style.theme_use('alt')
        
        self.setupUi()
    
    def setupUi(self):
        """Initialize and configure UI widgets"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        settingsFrame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settingsFrame, text='Settings')
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.setupApplicationsTable(settingsFrame)
    
    def setupApplicationsTable(self, parent):
        """Create a scrollable table showing all detected applications"""
        tableFrame = ttk.Frame(parent)
        tableFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        tableFrame.columnconfigure(0, weight=1)
        tableFrame.rowconfigure(1, weight=1)
        
        # Add button frame above the table headers
        buttonFrame = ttk.Frame(tableFrame)
        buttonFrame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=0, pady=(0, 5))
        
        # Add + button positioned above Application and Path headers
        # Position it at column 1 (after Row# column) to align with Application header
        addButton = ttk.Button(buttonFrame, text="+", command=self.showAddApplicationDialog, width=3)
        addButton.grid(row=0, column=1, padx=(50, 0), sticky=tk.W)
        
        columns = ('Row#', 'Application', 'Path')
        self.appTree = ttk.Treeview(tableFrame, columns=columns, show='headings', height=20)
        
        self.appTree.heading('Row#', text='Row#')
        self.appTree.heading('Application', text='Application')
        self.appTree.heading('Path', text='Path')
        
        self.appTree.column('Row#', width=50, anchor=tk.CENTER)
        self.appTree.column('Application', width=200, anchor=tk.W)
        self.appTree.column('Path', width=500, anchor=tk.W)
        
        self.appTree.bind('<Double-1>', self.onCellDoubleClick)
        
        scrollbar = ttk.Scrollbar(tableFrame, orient=tk.VERTICAL, command=self.appTree.yview)
        self.appTree.configure(yscrollcommand=scrollbar.set)
        
        self.appTree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        self.tableFrame = tableFrame
        
        self.populateApplications()
    
    def populateApplications(self):
        """Load applications from app_registry into the table"""
        for item in self.appTree.get_children():
            self.appTree.delete(item)
        
        for index, (appName, appPath) in enumerate(self.app_registry.apps):
            rowNumber = index + 1
            self.appTree.insert('', tk.END, values=(rowNumber, appName, appPath))
    
    def onCellDoubleClick(self, event):
        """Handle double-click on a cell to edit it"""
        try:
            region = self.appTree.identify_region(event.x, event.y)
            if region != 'cell':
                return
            
            column = self.appTree.identify_column(event.x)
            item = self.appTree.identify_row(event.y)
            
            if not item or not column:
                return
            
            try:
                colIndex = int(column.replace('#', ''))
            except (ValueError, AttributeError):
                return
            
            if colIndex == 1:
                return
            
            if colIndex not in (2, 3):
                return
            
            values = list(self.appTree.item(item, 'values'))
            
            if not values or len(values) < 3:
                return
            
            try:
                rowNumber = int(values[0])
            except (ValueError, IndexError):
                return
            
            appIndex = rowNumber - 1
            
            if appIndex < 0 or appIndex >= len(self.app_registry.apps):
                return
            
            appsColIndex = colIndex - 2
            columnName = ('Application', 'Path')[appsColIndex]
            
            self.editCell(item, colIndex, appsColIndex, columnName, values, appIndex)
        except Exception as e:
            print(f"Error in onCellDoubleClick: {e}")
            import traceback
            traceback.print_exc()
    
    def editCell(self, item, colIndex, appsColIndex, columnName, currentValues, appIndex):
        """Create an entry widget to edit a cell"""
        try:
            bbox = self.appTree.bbox(item, column=f'#{colIndex}')
            
            if not bbox:
                self.appTree.see(item)
                bbox = self.appTree.bbox(item, column=f'#{colIndex}')
                if not bbox:
                    print(f"Could not get bbox for item {item}, column #{colIndex}")
                    return
            
            currentValue = currentValues[colIndex - 1] if colIndex > 0 else ''
            
            editEntry = ttk.Entry(self.tableFrame)
            editEntry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
            editEntry.insert(0, str(currentValue))
            editEntry.select_range(0, tk.END)
            editEntry.focus()
            
            def saveEdit():
                """Save the edited value"""
                try:
                    newValue = editEntry.get().strip()
                    editEntry.destroy()
                    
                    newValues = list(currentValues)
                    newValues[colIndex - 1] = newValue
                    self.appTree.item(item, values=tuple(newValues))
                    
                    if 0 <= appIndex < len(self.app_registry.apps):
                        self.app_registry.apps[appIndex][appsColIndex] = newValue
                        self.app_registry.saveApplicationsToFile()
                        print(f"Updated appRegistry.apps[{appIndex}][{appsColIndex}] to: {newValue}")
                except Exception as e:
                    print(f"Error saving edit: {e}")
                    import traceback
                    traceback.print_exc()
            
            def cancelEdit():
                """Cancel editing"""
                editEntry.destroy()
            
            editEntry.bind('<Return>', lambda e: saveEdit())
            editEntry.bind('<Escape>', lambda e: cancelEdit())
            editEntry.bind('<FocusOut>', lambda e: saveEdit())
            
        except Exception as e:
            print(f"Error in editCell: {e}")
            import traceback
            traceback.print_exc()
        
    def run(self):
        """Start the UI mainloop"""
        self.root.mainloop()
    
    def showAddApplicationDialog(self):
        """Show a popup dialog to add a new application"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Application")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog on the parent window
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Application name field
        ttk.Label(dialog, text="Application:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        appEntry = ttk.Entry(dialog, width=40)
        appEntry.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        appEntry.focus()
        
        # Path field
        ttk.Label(dialog, text="Path:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        pathEntry = ttk.Entry(dialog, width=40)
        pathEntry.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        dialog.columnconfigure(1, weight=1)
        
        def confirm():
            """Handle confirm button click"""
            appName = appEntry.get().strip()
            appPath = pathEntry.get().strip()
            
            if not appName or not appPath:
                return
            
            # Add to appRegistry
            self.app_registry.apps.append([appName, appPath])
            
            # Save to cache
            self.app_registry.saveApplicationsToFile()
            
            # Refresh the table
            self.populateApplications()
            
            # Close dialog
            dialog.destroy()
        
        def cancel():
            """Handle cancel button click"""
            dialog.destroy()
        
        # Buttons
        buttonFrame = ttk.Frame(dialog)
        buttonFrame.grid(row=2, column=0, columnspan=2, pady=10)
        
        confirmButton = ttk.Button(buttonFrame, text="Confirm", command=confirm)
        confirmButton.pack(side=tk.LEFT, padx=5)
        
        cancelButton = ttk.Button(buttonFrame, text="Cancel", command=cancel)
        cancelButton.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to confirm
        appEntry.bind('<Return>', lambda e: confirm())
        pathEntry.bind('<Return>', lambda e: confirm())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def close(self):
        """Close the UI window"""
        self.root.destroy()
