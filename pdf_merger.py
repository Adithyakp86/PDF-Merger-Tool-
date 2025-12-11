import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import threading

# Try to import drag and drop functionality (optional)
try:
    from tkinter.dnd import DND_FILES
    DND_SUPPORTED = True
except ImportError:
    DND_SUPPORTED = False
# Configuration file path
CONFIG_FILE = "pdf_merger_config.json"

class PDFMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger Tool")
        self.root.geometry("600x500")
        self.root.minsize(600, 400)
        
        # Load configuration
        self.config = self.load_config()
        self.dark_mode = self.config.get("dark_mode", False)
        self.last_directory = self.config.get("last_directory", ".")
        
        # Create widgets first
        self.create_widgets()
        
        # Then set theme
        self.setup_theme()
        
        # Configure drag and drop
        self.setup_drag_and_drop()

    def load_config(self):
        """Load configuration from file"""
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_config(self):
        """Save configuration to file"""
        self.config["dark_mode"] = self.dark_mode
        self.config["last_directory"] = self.last_directory
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Could not save config: {e}")
    
    def setup_theme(self):
        """Setup light/dark theme"""
        self.style = ttk.Style()
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()
    
    def set_dark_theme(self):
        """Apply dark theme"""
        self.root.configure(bg="#2e2e2e")
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure("TLabel", background="#2e2e2e", foreground="white")
        self.style.configure("TButton", background="#444444", foreground="white")
        self.style.map("TButton", background=[('active', '#555555')])
        # Only configure listbox if it exists
        if hasattr(self, 'file_listbox'):
            self.file_listbox.configure(bg="#3e3e3e", fg="white", selectbackground="#555555")
        if hasattr(self, 'status_label'):
            self.status_label.configure(background="#2e2e2e", foreground="white")
    
    def set_light_theme(self):
        """Apply light theme"""
        self.root.configure(bg="white")
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", background="white", foreground="black")
        self.style.configure("TButton", background="#e0e0e0", foreground="black")
        self.style.map("TButton", background=[('active', '#d0d0d0')])
        # Only configure listbox if it exists
        if hasattr(self, 'file_listbox'):
            self.file_listbox.configure(bg="white", fg="black", selectbackground="#a0c0ff")
        if hasattr(self, 'status_label'):
            self.status_label.configure(background="white", foreground="black")
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        self.setup_theme()
        self.save_config()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF Merger Tool", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Add PDF button
        add_button = ttk.Button(buttons_frame, text="Add PDF Files", command=self.add_files)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Theme toggle button
        theme_button = ttk.Button(buttons_frame, text="Toggle Theme", command=self.toggle_theme)
        theme_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=3, padx=(10, 0), sticky=(tk.N, tk.S))
        
        move_up_btn = ttk.Button(control_frame, text="Move Up", command=self.move_up)
        move_up_btn.pack(fill=tk.X, pady=(0, 5))
        
        move_down_btn = ttk.Button(control_frame, text="Move Down", command=self.move_down)
        move_down_btn.pack(fill=tk.X, pady=(0, 5))
        
        remove_btn = ttk.Button(control_frame, text="Remove Selected", command=self.remove_selected)
        remove_btn.pack(fill=tk.X, pady=(0, 5))
        
        clear_btn = ttk.Button(control_frame, text="Clear All", command=self.clear_all)
        clear_btn.pack(fill=tk.X, pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Total files: 0 | Total pages: 0")
        self.status_label.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Merge button
        merge_button = ttk.Button(main_frame, text="Merge PDFs", command=self.merge_pdfs_threaded)
        merge_button.grid(row=5, column=0, columnspan=4, pady=(0, 10))
        
        # Output label
        self.output_label = ttk.Label(main_frame, text="Output: merged.pdf")
        self.output_label.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        # Update status
        self.update_status()
    
    def setup_drag_and_drop(self):
        """Setup drag and drop functionality"""
        if DND_SUPPORTED:
            try:
                # Register drag and drop
                self.file_listbox.drop_target_register(DND_FILES)
                self.file_listbox.dnd_bind('<<Drop>>', self.on_drop)
            except Exception as e:
                print(f"Drag and drop not available: {e}")
        else:
            print("Drag and drop functionality not supported in this Python version")
    
    def on_drop(self, event):
        """Handle file drop event"""
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith('.pdf'):
                self.file_listbox.insert(tk.END, file)
        self.update_status()
    
    def add_files(self):
        """Add PDF files to the list"""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")],
            initialdir=self.last_directory
        )
        
        if files:
            # Update last directory
            self.last_directory = os.path.dirname(files[0])
            self.save_config()
            
            # Add files to listbox
            for file in files:
                self.file_listbox.insert(tk.END, file)
            
            self.update_status()
    
    def move_up(self):
        """Move selected items up in the list"""
        selections = self.file_listbox.curselection()
        if not selections:
            return
            
        # Check if first item is selected
        if 0 in selections:
            return
            
        # Move items up
        for index in selections:
            text = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index - 1, text)
            
        # Reselect moved items
        for index in selections:
            self.file_listbox.select_set(index - 1)
    
    def move_down(self):
        """Move selected items down in the list"""
        selections = self.file_listbox.curselection()
        if not selections:
            return
            
        # Check if last item is selected
        if self.file_listbox.size() - 1 in selections:
            return
            
        # Move items down (in reverse order to maintain indices)
        for index in reversed(selections):
            text = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index + 1, text)
            
        # Reselect moved items
        for index in selections:
            self.file_listbox.select_set(index + 1)
    
    def remove_selected(self):
        """Remove selected items from the list"""
        selections = self.file_listbox.curselection()
        if not selections:
            return
            
        # Delete in reverse order to maintain indices
        for index in reversed(selections):
            self.file_listbox.delete(index)
            
        self.update_status()
    
    def clear_all(self):
        """Clear all items from the list"""
        self.file_listbox.delete(0, tk.END)
        self.update_status()
    
    def update_status(self):
        """Update status label with file count and page count"""
        file_count = self.file_listbox.size()
        page_count = 0
        
        # Count pages in each PDF
        for i in range(file_count):
            file_path = self.file_listbox.get(i)
            try:
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    page_count += len(reader.pages)
            except Exception:
                # Skip invalid files for page count
                pass
        
        self.status_label.configure(text=f"Total files: {file_count} | Total pages: {page_count}")
    
    def merge_pdfs_threaded(self):
        """Start merging process in a separate thread"""
        # Disable buttons during merge
        self.progress.start()
        thread = threading.Thread(target=self.merge_pdfs)
        thread.start()
    
    def merge_pdfs(self):
        """Merge selected PDF files"""
        # Get file list
        file_count = self.file_listbox.size()
        if file_count == 0:
            self.show_message("No files selected", "Please add PDF files to merge.", "warning")
            self.progress.stop()
            return
            
        files = [self.file_listbox.get(i) for i in range(file_count)]
        
        # Create PDF writer
        writer = PyPDF2.PdfWriter()
        total_pages = 0
        error_files = []
        
        # Process each file
        for file_path in files:
            try:
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    # Add all pages to writer
                    for page in reader.pages:
                        writer.add_page(page)
                    total_pages += len(reader.pages)
            except Exception as e:
                error_files.append((file_path, str(e)))
        
        # Check for errors
        if error_files:
            error_msg = "Errors occurred with the following files:\n\n"
            for file_path, error in error_files[:3]:  # Show first 3 errors
                error_msg += f"{os.path.basename(file_path)}: {error}\n"
            if len(error_files) > 3:
                error_msg += f"\n... and {len(error_files) - 3} more files."
                
            self.show_message("Merge Errors", error_msg, "error")
            
            # If all files failed, stop here
            if len(error_files) == len(files):
                self.progress.stop()
                return
        
        # Write merged PDF
        try:
            with open("merged.pdf", 'wb') as f:
                writer.write(f)
                
            # Show success message
            self.show_message(
                "Success", 
                f"PDFs merged successfully!\nOutput: merged.pdf\nTotal pages: {total_pages}", 
                "info"
            )
        except Exception as e:
            self.show_message("Merge Failed", f"Failed to save merged PDF:\n{str(e)}", "error")
        
        self.progress.stop()
    
    def show_message(self, title, message, msg_type="info"):
        """Show message box in the main thread"""
        self.root.after(0, lambda: self._show_message(title, message, msg_type))
    
    def _show_message(self, title, message, msg_type):
        """Internal method to show message box"""
        if msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)


def merge_pdfs_cli():
    """CLI mode for merging PDFs"""
    print("PDF Merger Tool - CLI Mode")
    print("=" * 30)
    
    # Get file paths from user
    file_paths = []
    print("Enter PDF file paths (press Enter with empty input to finish):")
    
    while True:
        path = input("PDF file path: ").strip()
        if not path:
            break
            
        if os.path.isfile(path) and path.lower().endswith('.pdf'):
            file_paths.append(path)
        else:
            print(f"Invalid file or not a PDF: {path}")
    
    if not file_paths:
        print("No valid PDF files provided.")
        return
    
    print("\nLoading PDFs...")
    
    # Create PDF writer
    writer = PyPDF2.PdfWriter()
    total_pages = 0
    error_files = []
    
    print("Merging...")
    
    # Process each file
    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                # Add all pages to writer
                for page in reader.pages:
                    writer.add_page(page)
                total_pages += len(reader.pages)
        except Exception as e:
            error_files.append((file_path, str(e)))
    
    # Check for errors
    if error_files:
        print("\nErrors occurred with the following files:")
        for file_path, error in error_files:
            print(f"  {os.path.basename(file_path)}: {error}")
            
        # If all files failed, stop here
        if len(error_files) == len(file_paths):
            print("All files failed to process. Exiting.")
            return
    
    # Write merged PDF
    try:
        with open("merged_output.pdf", 'wb') as f:
            writer.write(f)
        print(f"\nDone! File saved as merged_output.pdf")
        print(f"Total pages merged: {total_pages}")
    except Exception as e:
        print(f"\nFailed to save merged PDF: {e}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        merge_pdfs_cli()
    else:
        # GUI mode
        root = tk.Tk()
        app = PDFMergerGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()