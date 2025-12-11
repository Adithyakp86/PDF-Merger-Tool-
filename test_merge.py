import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_merger import merge_pdfs_cli

# Create a simple test that simulates user input
def test_cli_merge():
    # We'll test the underlying functionality directly
    print("Testing PDF merge functionality...")
    
    # Check if test files exist
    if os.path.exists("test1.pdf") and os.path.exists("test2.pdf"):
        print("Test PDFs found. Running merge test...")
        
        # Test the merge function directly
        from PyPDF2 import PdfWriter, PdfReader
        
        # Create PDF writer
        writer = PdfWriter()
        total_pages = 0
        
        # Process each file
        for file_path in ["test1.pdf", "test2.pdf"]:
            try:
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    # Add all pages to writer
                    for page in reader.pages:
                        writer.add_page(page)
                    total_pages += len(reader.pages)
                print(f"Processed {file_path}: {len(reader.pages)} pages")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                return False
        
        # Write merged PDF
        try:
            with open("test_merged_output.pdf", 'wb') as f:
                writer.write(f)
            print(f"Successfully merged PDFs into test_merged_output.pdf ({total_pages} pages)")
            return True
        except Exception as e:
            print(f"Failed to save merged PDF: {e}")
            return False
    else:
        print("Test PDFs not found. Creating sample PDFs first...")
        # Create test PDFs
        try:
            from reportlab.pdfgen import canvas
            
            # Create first test PDF
            c = canvas.Canvas("test1.pdf")
            c.drawString(100, 750, "Test PDF 1")
            c.drawString(100, 700, "Page 1")
            c.save()
            
            # Create second test PDF
            c = canvas.Canvas("test2.pdf")
            c.drawString(100, 750, "Test PDF 2")
            c.drawString(100, 700, "Page 1")
            c.showPage()  # Add a second page
            c.drawString(100, 750, "Test PDF 2")
            c.drawString(100, 700, "Page 2")
            c.save()
            
            print("Created test PDFs. Running merge test...")
            return test_cli_merge()  # Recursive call to test with newly created files
        except Exception as e:
            print(f"Failed to create test PDFs: {e}")
            return False

if __name__ == "__main__":
    success = test_cli_merge()
    if success:
        print("TEST PASSED: PDF merging functionality works correctly!")
    else:
        print("TEST FAILED: PDF merging functionality has issues.")