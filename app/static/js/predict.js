    document.addEventListener('DOMContentLoaded', function() {
        const fileInput = document.getElementById('file');
        const preview = document.getElementById('preview');
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');
        const dropArea = document.getElementById('drop-area');
        const form = document.getElementById('predict-form');
        const resultDisplay = document.getElementById('result-display');
    
        function handleFile(file) {
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    fileName.textContent = file.name;
                    fileSize.textContent = `Size: ${(file.size / 1024).toFixed(2)} KB`;
                    checkFormCompletion();
                }
                reader.readAsDataURL(file);
            }
        }
    
        function submitForm() {
            const formData = new FormData(form);
            resultDisplay.innerHTML = '<p>Processing... Please wait.</p>';
            
            fetch('/predict', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 400) {
                        return response.json().then(data => {
                            throw new Error(data.error || 'Bad Request');
                        });
                    }
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }

                // Check if treatment is available
                if (data.treatment) {
                    resultDisplay.innerHTML = `
                        <p>Prediction: ${data.prediction}</p>
                        <p>Confidence: ${data.confidence}%</p>
                        <h3>Treatment Details</h3>
                        <p><strong>Tumor Type:</strong> ${data.treatment.tumor_type}</p>
                        <p><strong>Description:</strong> ${data.treatment.description}</p>
                        <p><strong>Recommended Medication:</strong> ${data.treatment.recommended_medication}</p>
                        <p><strong>Duration:</strong> ${data.treatment.duration}</p>
                        <p><strong>Side Effects:</strong> ${data.treatment.side_effects}</p>
                    `;
                } else {
                    resultDisplay.innerHTML = `
                        <p>Prediction: ${data.prediction}</p>
                        <p>Confidence: ${data.confidence}%</p>
                        <p>No treatment information available.</p>
                    `;
                }
            })
            .catch(error => {
                console.error('Prediction error:', error);
                resultDisplay.innerHTML = `<p>Error: ${error.message}</p>`;
            });
        }
    
        function checkFormCompletion() {
            const requiredFields = form.querySelectorAll('[required]');
            const allFilled = Array.from(requiredFields).every(field => field.value.trim() !== '');
            
            // Automatically submit the form if all required fields are filled and a file is selected
            if (allFilled && fileInput.files.length > 0) {
                submitForm();
            }
        }
    
        fileInput.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });
    
        // Add event listeners to all form inputs
        const formInputs = form.querySelectorAll('input, select, textarea');
        formInputs.forEach(input => {
            input.addEventListener('change', checkFormCompletion);
        });
    
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });
    
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
    
        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, highlight, false);
        });
    
        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, unhighlight, false);
        });
    
        function highlight(e) {
            dropArea.classList.add('highlight');
        }
    
        function unhighlight(e) {
            dropArea.classList.remove('highlight');
        }
    
        dropArea.addEventListener('drop', handleDrop, false);
    
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const file = dt.files[0];
            fileInput.files = dt.files;
            handleFile(file);
        }
    });
