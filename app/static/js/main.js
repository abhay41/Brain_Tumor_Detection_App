document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.classList.remove('show');
            setTimeout(function() {
                message.remove();
            }, 150);
        }, 5000);
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggle = document.getElementById('profileDropdown');

    // Toggle dropdown menu on click
    dropdownToggle.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default anchor behavior
        const dropdownMenu = document.getElementById('dropdownMenu');

        // Toggle visibility
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });

    // Close dropdown if clicked outside of it
    window.onclick = function(event) {
        const dropdownMenu = document.getElementById('dropdownMenu');
        
        // Check if the clicked target is not the dropdown toggle or inside the dropdown
        if (dropdownMenu && !dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.style.display = 'none'; // Hide dropdown
        }
    };
});

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('.file-input');
    const previewSection = document.querySelector('.preview-section');
    const imagePreview = document.getElementById('imagePreview');
    const uploadArea = document.querySelector('.upload-area');
    
    // Image adjustment variables
    let scale = 1;
    let rotation = 0;
    let isDragging = false;
    let startPos = { x: 0, y: 0 };
    let currentPos = { x: 0, y: 0 };

    // Control buttons
    const zoomIn = document.getElementById('zoomIn');
    const zoomOut = document.getElementById('zoomOut');
    const rotateLeft = document.getElementById('rotateLeft');
    const rotateRight = document.getElementById('rotateRight');

    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            previewImage(file);
        }
    });

    // Image preview function
    function previewImage(file) {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewSection.style.display = 'block';
                // Reset transformations
                scale = 1;
                rotation = 0;
                currentPos = { x: 0, y: 0 };
                updateImageTransform();
            }
            reader.readAsDataURL(file);
        } else {
            alert('Please select an image file');
        }
    }

    // Image adjustment functions
    function updateImageTransform() {
        imagePreview.style.transform = `
            rotate(${rotation}deg) 
            scale(${scale}) 
            translate(${currentPos.x}px, ${currentPos.y}px)
        `;
    }

    // Zoom controls
    zoomIn.addEventListener('click', () => {
        scale = Math.min(scale + 0.1, 3);
        updateImageTransform();
    });

    zoomOut.addEventListener('click', () => {
        scale = Math.max(scale - 0.1, 0.5);
        updateImageTransform();
    });

    // Rotation controls
    rotateLeft.addEventListener('click', () => {
        rotation = (rotation - 90) % 360;
        updateImageTransform();
    });

    rotateRight.addEventListener('click', () => {
        rotation = (rotation + 90) % 360;
        updateImageTransform();
    });

    // Drag functionality
    imagePreview.addEventListener('mousedown', (e) => {
        isDragging = true;
        startPos = {
            x: e.clientX - currentPos.x,
            y: e.clientY - currentPos.y
        };
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        
        currentPos = {
            x: e.clientX - startPos.x,
            y: e.clientY - startPos.y
        };
        updateImageTransform();
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            fileInput.files = e.dataTransfer.files;
            previewImage(file);
        }
    });
});
