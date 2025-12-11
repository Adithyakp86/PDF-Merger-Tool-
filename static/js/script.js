document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const dropArea = document.getElementById('dropArea');
    const fileInput = document.getElementById('fileInput');
    const selectFilesBtn = document.getElementById('selectFilesBtn');
    const filesList = document.getElementById('filesList');
    const fileStats = document.getElementById('fileStats');
    const moveUpBtn = document.getElementById('moveUpBtn');
    const moveDownBtn = document.getElementById('moveDownBtn');
    const removeSelectedBtn = document.getElementById('removeSelectedBtn');
    const clearAllBtn = document.getElementById('clearAllBtn');
    const mergeBtn = document.getElementById('mergeBtn');
    const themeToggle = document.getElementById('theme-toggle');
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const outputInfo = document.getElementById('outputInfo');
    const downloadBtn = document.getElementById('downloadBtn');
    const editSection = document.getElementById('editSection');
    const pageNumber = document.getElementById('pageNumber');
    const removePageBtn = document.getElementById('removePageBtn');
    const rotate90Btn = document.getElementById('rotate90Btn');
    const rotate180Btn = document.getElementById('rotate180Btn');
    const rotate270Btn = document.getElementById('rotate270Btn');
    const textToAdd = document.getElementById('textToAdd');
    const textX = document.getElementById('textX');
    const textY = document.getElementById('textY');
    const addTextBtn = document.getElementById('addTextBtn');
    const editedOutput = document.getElementById('editedOutput');
    const editedPath = document.getElementById('editedPath');
    const downloadEditedBtn = document.getElementById('downloadEditedBtn');
    
    // State
    let uploadedFiles = [];
    let mergedFilePath = '';
    
    // Event Listeners
    selectFilesBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    moveUpBtn.addEventListener('click', moveSelectedUp);
    moveDownBtn.addEventListener('click', moveSelectedDown);
    removeSelectedBtn.addEventListener('click', removeSelectedFiles);
    clearAllBtn.addEventListener('click', clearAllFiles);
    mergeBtn.addEventListener('click', mergePDFs);
    themeToggle.addEventListener('click', toggleTheme);
    downloadBtn.addEventListener('click', downloadMergedPDF);
    removePageBtn.addEventListener('click', removePage);
    rotate90Btn.addEventListener('click', () => rotatePage(90));
    rotate180Btn.addEventListener('click', () => rotatePage(180));
    rotate270Btn.addEventListener('click', () => rotatePage(270));
    addTextBtn.addEventListener('click', addTextToPDF);
    downloadEditedBtn.addEventListener('click', downloadEditedPDF);
    
    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    dropArea.addEventListener('drop', handleDrop, false);
    
    // Functions
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight() {
        dropArea.classList.add('highlight');
    }
    
    function unhighlight() {
        dropArea.classList.remove('highlight');
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }
    
    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }
    
    function handleFiles(files) {
        [...files].forEach(uploadFile);
    }
    
    function uploadFile(file) {
        if (file.type !== 'application/pdf') {
            alert('Please select only PDF files.');
            return;
        }
        
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('files[]', file);
        
        // Upload file via AJAX
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            
            // Add uploaded files to the list
            data.files.forEach(fileInfo => {
                uploadedFiles.push(fileInfo);
            });
            
            renderFileList();
            updateFileStats();
            updateButtonStates();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error uploading file.');
        });
    }
    
    function renderFileList() {
        filesList.innerHTML = '';
        
        uploadedFiles.forEach((file, index) => {
            const li = document.createElement('li');
            li.className = 'file-item';
            li.dataset.index = index;
            
            li.innerHTML = `
                <input type="checkbox" data-index="${index}">
                <span class="file-name">${file.name}</span>
                <span class="file-pages">(loading...)</span>
            `;
            
            li.addEventListener('click', function(e) {
                if (e.target.tagName !== 'INPUT') {
                    const checkbox = this.querySelector('input[type="checkbox"]');
                    checkbox.checked = !checkbox.checked;
                    updateButtonStates();
                }
            });
            
            filesList.appendChild(li);
            
            // Get page count for the file
            getPageCount(file.path, index);
        });
    }
    
    function getPageCount(filePath, index) {
        // In a real implementation, we would get this from the server
        // For now, we'll simulate it
        setTimeout(() => {
            const fileItems = document.querySelectorAll('.file-item');
            if (fileItems[index]) {
                const pagesSpan = fileItems[index].querySelector('.file-pages');
                // Simulate getting page count (in a real app, this would come from server)
                const pageCount = Math.floor(Math.random() * 10) + 1;
                pagesSpan.textContent = `(${pageCount} pages)`;
                updateFileStats();
            }
        }, 500);
    }
    
    function updateFileStats() {
        const totalFiles = uploadedFiles.length;
        // In a real implementation, we would calculate actual page count
        const totalPages = totalFiles * 5; // Simulated
        fileStats.textContent = `Total files: ${totalFiles} | Total pages: ${totalPages}`;
    }
    
    function updateButtonStates() {
        const selectedCheckboxes = document.querySelectorAll('.file-item input[type="checkbox"]:checked');
        const hasSelection = selectedCheckboxes.length > 0;
        const hasFiles = uploadedFiles.length > 0;
        
        moveUpBtn.disabled = !hasSelection || selectedCheckboxes[0].closest('.file-item').dataset.index === '0';
        moveDownBtn.disabled = !hasSelection || selectedCheckboxes[selectedCheckboxes.length - 1].closest('.file-item').dataset.index === String(uploadedFiles.length - 1);
        removeSelectedBtn.disabled = !hasSelection;
        clearAllBtn.disabled = !hasFiles;
        mergeBtn.disabled = !hasFiles;
    }
    
    function moveSelectedUp() {
        const selectedCheckboxes = document.querySelectorAll('.file-item input[type="checkbox"]:checked');
        
        // Sort by index to move in correct order
        const indices = Array.from(selectedCheckboxes)
            .map(cb => parseInt(cb.closest('.file-item').dataset.index))
            .sort((a, b) => a - b);
        
        // Move each selected item up
        for (let i = 0; i < indices.length; i++) {
            const index = indices[i];
            if (index > 0) {
                // Swap in array
                [uploadedFiles[index - 1], uploadedFiles[index]] = [uploadedFiles[index], uploadedFiles[index - 1]];
            }
        }
        
        renderFileList();
        updateButtonStates();
        
        // Reorder on server
        reorderFiles();
    }
    
    function moveSelectedDown() {
        const selectedCheckboxes = document.querySelectorAll('.file-item input[type="checkbox"]:checked');
        
        // Sort by index in descending order to move in correct order
        const indices = Array.from(selectedCheckboxes)
            .map(cb => parseInt(cb.closest('.file-item').dataset.index))
            .sort((a, b) => b - a);
        
        // Move each selected item down
        for (let i = 0; i < indices.length; i++) {
            const index = indices[i];
            if (index < uploadedFiles.length - 1) {
                // Swap in array
                [uploadedFiles[index], uploadedFiles[index + 1]] = [uploadedFiles[index + 1], uploadedFiles[index]];
            }
        }
        
        renderFileList();
        updateButtonStates();
        
        // Reorder on server
        reorderFiles();
    }
    
    function removeSelectedFiles() {
        const selectedCheckboxes = document.querySelectorAll('.file-item input[type="checkbox"]:checked');
        const indicesToRemove = Array.from(selectedCheckboxes)
            .map(cb => parseInt(cb.closest('.file-item').dataset.index))
            .sort((a, b) => b - a); // Sort descending to remove from end first
        
        // Remove files from array
        indicesToRemove.forEach(index => {
            // Delete file on server
            fetch('/delete_file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ path: uploadedFiles[index].path })
            });
            
            uploadedFiles.splice(index, 1);
        });
        
        renderFileList();
        updateFileStats();
        updateButtonStates();
    }
    
    function clearAllFiles() {
        // Clear all files on server
        fetch('/clear_all', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                uploadedFiles = [];
                renderFileList();
                updateFileStats();
                updateButtonStates();
            } else {
                alert('Error clearing files: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error clearing files.');
        });
    }
    
    function reorderFiles() {
        fetch('/reorder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ order: uploadedFiles })
        })
        .then(response => response.json())
        .then(data => {
            if (data.files) {
                uploadedFiles = data.files;
            }
        })
        .catch(error => {
            console.error('Error reordering files:', error);
        });
    }
    
    function mergePDFs() {
        // Show progress
        progressContainer.style.display = 'block';
        progressBar.style.width = '30%';
        
        // Send merge request
        fetch('/merge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ files: uploadedFiles })
        })
        .then(response => {
            progressBar.style.width = '70%';
            return response.json();
        })
        .then(data => {
            progressBar.style.width = '100%';
            
            if (data.error) {
                alert('Merge error: ' + data.error);
                progressContainer.style.display = 'none';
                return;
            }
            
            // Store merged file path
            mergedFilePath = data.output_path;
            
            // Show success message
            setTimeout(() => {
                progressContainer.style.display = 'none';
                outputInfo.style.display = 'block';
                downloadBtn.style.display = 'inline-block';
                
                // Show edit section
                editSection.style.display = 'block';
                
                alert(`PDFs merged successfully!\nTotal pages: ${data.total_pages}`);
            }, 500);
        })
        .catch(error => {
            console.error('Error:', error);
            progressContainer.style.display = 'none';
            alert('Error merging PDFs.');
        });
    }
    
    function downloadMergedPDF() {
        // Redirect to download endpoint
        window.location.href = '/download/merged.pdf';
    }
    
    function removePage() {
        if (!mergedFilePath) {
            alert('No merged PDF available for editing.');
            return;
        }
        
        const pageNum = parseInt(pageNumber.value) - 1; // Convert to 0-based index
        
        fetch('/edit/remove_page', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pdf_path: mergedFilePath,
                page_num: pageNum
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error removing page: ' + data.error);
                return;
            }
            
            // Show edited output
            editedPath.textContent = data.output_path;
            editedOutput.style.display = 'block';
            alert('Page removed successfully!');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error removing page.');
        });
    }
    
    function rotatePage(rotation) {
        if (!mergedFilePath) {
            alert('No merged PDF available for editing.');
            return;
        }
        
        const pageNum = parseInt(pageNumber.value) - 1; // Convert to 0-based index
        
        fetch('/edit/rotate_page', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pdf_path: mergedFilePath,
                page_num: pageNum,
                rotation: rotation
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error rotating page: ' + data.error);
                return;
            }
            
            // Show edited output
            editedPath.textContent = data.output_path;
            editedOutput.style.display = 'block';
            alert(`Page rotated ${rotation} degrees successfully!`);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error rotating page.');
        });
    }
    
    function addTextToPDF() {
        if (!mergedFilePath) {
            alert('No merged PDF available for editing.');
            return;
        }
        
        const text = textToAdd.value;
        if (!text) {
            alert('Please enter text to add.');
            return;
        }
        
        const pageNum = parseInt(pageNumber.value) - 1; // Convert to 0-based index
        const x = parseInt(textX.value);
        const y = parseInt(textY.value);
        
        fetch('/edit/add_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pdf_path: mergedFilePath,
                text: text,
                page_num: pageNum,
                x: x,
                y: y
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error adding text: ' + data.error);
                return;
            }
            
            // Show edited output
            editedPath.textContent = data.output_path;
            editedOutput.style.display = 'block';
            alert('Text added successfully!');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding text.');
        });
    }
    
    function downloadEditedPDF() {
        // Get the filename from the path
        const filename = editedPath.textContent.split('/').pop().split('\\').pop();
        // Redirect to download endpoint
        window.location.href = `/download/${filename}`;
    }
    
    function toggleTheme() {
        fetch('/toggle_theme', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.dark_mode) {
                document.body.classList.add('dark-mode');
            } else {
                document.body.classList.remove('dark-mode');
            }
        })
        .catch(error => {
            console.error('Error toggling theme:', error);
        });
    }
    
    // Initialize
    updateButtonStates();
});