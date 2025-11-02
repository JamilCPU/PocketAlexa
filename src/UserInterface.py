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
        tableFrame.rowconfigure(0, weight=1)
        
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
        
        self.appTree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
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
    
    def close(self):
        """Close the UI window"""
        self.root.destroy()
