# PDF Merger Tool

A complete PDF merging tool with Command-Line Interface (CLI), Graphical User Interface (GUI), and Web Interface modes built using Python.

## Features

### Core Functionality
- Select multiple PDF files
- Rearrange file order (move up/down)
- Merge PDFs into a single output file
- Save output as `merged.pdf` (GUI/Web) or `merged_output.pdf` (CLI)
- Show total number of pages merged
- Handle corrupted or empty PDFs gracefully

### GUI Mode Features
- Clean, modern user interface with Tkinter
- Drag and drop support for adding PDF files
- Dark/light mode toggle with persistent settings
- Remembers last used folder
- Progress indicator during merging
- Success/error popup notifications
- File management controls (move, remove, clear)

### CLI Mode Features
- Simple command-line interface
- Easy file path input
- Clear status messages

### Web Interface Features
- Browser-based interface accessible from any device
- Drag and drop support for adding PDF files
- Dark/light mode toggle with persistent settings
- Responsive design for desktop and mobile devices
- Real-time file management and reordering
- Progress indicators during merging
- Direct download of merged PDF
- **PDF Editing Capabilities**:
  - Remove pages from merged PDFs
  - Rotate pages (90°, 180°, 270°)
  - Add text to specific positions on pages

## Requirements

- Python 3.6+
- PyPDF2
- Pillow (PIL)
- Flask
- ReportLab
- Tkinter (usually included with Python)

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### GUI Mode
Run the tool without any arguments to launch the graphical interface:
```
python pdf_merger.py
```

### CLI Mode
Run the tool with the `--cli` flag to use the command-line interface:
```
python pdf_merger.py --cli
```

### Web Interface Mode
Run the web application:
```
python web_pdf_merger.py
```
Then open your browser and navigate to `http://127.0.0.1:5000`

## How to Use the GUI

1. Click "Add PDF Files" to select PDF files or drag and drop PDF files into the window
2. Use "Move Up" and "Move Down" buttons to reorder files as needed
3. Use "Remove Selected" to remove specific files or "Clear All" to remove all files
4. Click "Merge PDFs" to combine the selected files
5. The merged PDF will be saved as `merged.pdf` in the same directory
6. Toggle between light and dark mode using the "Toggle Theme" button

## How to Use the Web Interface

1. Open your browser and go to `http://127.0.0.1:5000`
2. Click "Select PDF Files" or drag and drop PDF files into the upload area
3. Use "Move Up" and "Move Down" buttons to reorder files as needed
4. Use "Remove Selected" to remove specific files or "Clear All" to remove all files
5. Click "Merge PDFs" to combine the selected files
6. Download the merged PDF using the "Download Merged PDF" button
7. **After merging, use the PDF Editing Options**:
   - Enter the page number you want to edit
   - Remove pages with "Remove Page" button
   - Rotate pages with "Rotate" buttons
   - Add text by entering text and position, then clicking "Add Text"
8. Download the edited PDF using the "Download Edited PDF" button
9. Toggle between light and dark mode using the "Toggle Theme" button

## How to Use the CLI

1. Run the tool with the `--cli` flag
2. Enter the full paths to the PDF files you want to merge (one at a time)
3. Press Enter with an empty input to finish adding files
4. The merged PDF will be saved as `merged_output.pdf` in the same directory

## Configuration

The tool saves user preferences in `pdf_merger_config.json`:
- Last used directory
- Theme preference (light/dark mode)

## Error Handling

The tool provides clear error messages for:
- No files selected
- Invalid PDF files
- Files locked by another program
- Merge failures

## License

This project is open source and available under the MIT License.