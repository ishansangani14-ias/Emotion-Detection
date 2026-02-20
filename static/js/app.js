// Adaptive Multimodal Emotion Detection System - Frontend JavaScript

// Global state
let currentMode = 'multimodal';
let currentPrediction = null;
let uploadedImage = null;
let cameraStream = null;
let cameraMode = 'upload'; // 'upload' or 'camera'
let isLiveDetecting = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadQTable();
    loadStatistics();
    
    // Refresh stats every 5 seconds
    setInterval(loadStatistics, 5000);
});

// Initialize event listeners
function initializeEventListeners() {
    // Mode selector
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => handleModeChange(btn.dataset.mode));
    });
    
    // Camera/Upload toggle
    document.getElementById('upload-mode-btn').addEventListener('click', () => switchToUploadMode());
    document.getElementById('camera-mode-btn').addEventListener('click', () => switchToCameraMode());
    
    // Camera controls
    document.getElementById('start-camera-btn').addEventListener('click', startCamera);
    document.getElementById('stop-camera-btn').addEventListener('click', stopCamera);
    
    // Image upload
    const uploadArea = document.getElementById('upload-area');
    const imageInput = document.getElementById('image-input');
    
    uploadArea.addEventListener('click', () => imageInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#FF6B35';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#3A3A3A';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#3A3A3A';
        const file = e.dataTransfer.files[0];
        if (file) handleImageUpload(file);
    });
    
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleImageUpload(file);
    });
    
    // Predict button
    document.getElementById('predict-btn').addEventListener('click', handlePredict);
    
    // Feedback buttons
    document.getElementById('feedback-yes').addEventListener('click', () => handleFeedback(true));
    document.getElementById('feedback-no').addEventListener('click', () => handleFeedback(false));
    document.getElementById('submit-correction').addEventListener('click', submitCorrection);
}

// Switch to upload mode
function switchToUploadMode() {
    cameraMode = 'upload';
    document.getElementById('upload-mode-btn').classList.add('active');
    document.getElementById('camera-mode-btn').classList.remove('active');
    document.getElementById('upload-area').style.display = 'block';
    document.getElementById('camera-area').style.display = 'none';
    stopCamera();
}

// Switch to camera mode
function switchToCameraMode() {
    cameraMode = 'camera';
    document.getElementById('camera-mode-btn').classList.add('active');
    document.getElementById('upload-mode-btn').classList.remove('active');
    document.getElementById('upload-area').style.display = 'none';
    document.getElementById('camera-area').style.display = 'block';
}

// Start camera
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { 
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            } 
        });
        
        cameraStream = stream;
        const video = document.getElementById('camera-video');
        video.srcObject = stream;
        
        // Show/hide buttons
        document.getElementById('start-camera-btn').style.display = 'none';
        document.getElementById('stop-camera-btn').style.display = 'inline-flex';
        
        // Start live detection for face-only mode
        if (currentMode === 'face') {
            startLiveDetection();
        }
        
    } catch (error) {
        showError('Could not access camera: ' + error.message);
    }
}

// Stop camera
function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
        
        const video = document.getElementById('camera-video');
        video.srcObject = null;
        
        // Show/hide buttons
        document.getElementById('start-camera-btn').style.display = 'inline-flex';
        document.getElementById('stop-camera-btn').style.display = 'none';
        
        // Stop live detection
        isLiveDetecting = false;
        document.getElementById('live-prediction').style.display = 'none';
    }
}

// Start live detection
function startLiveDetection() {
    if (currentMode !== 'face') return;
    
    isLiveDetecting = true;
    document.getElementById('live-prediction').style.display = 'block';
    
    // Continuous real-time detection
    const detectLoop = async () => {
        if (!isLiveDetecting || !cameraStream) {
            return;
        }
        
        try {
            // Capture frame from video
            const imageBlob = await captureFrame();
            
            // Convert blob to file for proper upload
            const imageFile = new File([imageBlob], 'camera-capture.jpg', { type: 'image/jpeg' });
            
            // Predict emotion
            const response = await predictFace(imageFile);
            
            // Update live display with smooth transition
            document.querySelector('.live-emotion').textContent = response.emotion.toUpperCase();
            document.querySelector('.live-confidence').textContent = 
                `Confidence: ${(response.confidence * 100).toFixed(1)}%`;
            
            // Update main results display automatically
            currentPrediction = response;
            displayResults(response);
            
            // Hide feedback section during live detection
            document.getElementById('feedback-section').style.display = 'none';
            
        } catch (error) {
            console.error('Live detection error:', error);
            // Show error in live display
            document.querySelector('.live-emotion').textContent = 'ERROR';
            document.querySelector('.live-confidence').textContent = error.message;
        }
        
        // Continue loop with 500ms delay for smooth real-time updates
        if (isLiveDetecting) {
            setTimeout(detectLoop, 500);
        }
    };
    
    // Start the detection loop
    detectLoop();
}

// Capture frame from video
async function captureFrame() {
    const video = document.getElementById('camera-video');
    const canvas = document.getElementById('camera-canvas');
    const context = canvas.getContext('2d');
    
    // Set canvas size to match video
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    
    // Draw current video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Convert to blob with proper JPEG format
    return new Promise((resolve, reject) => {
        canvas.toBlob((blob) => {
            if (blob) {
                resolve(blob);
            } else {
                reject(new Error('Failed to capture frame'));
            }
        }, 'image/jpeg', 0.95);
    });
}

// Capture and predict
async function captureAndPredict() {
    try {
        showLoading(true);
        
        const imageBlob = await captureFrame();
        uploadedImage = new File([imageBlob], 'camera-capture.jpg', { type: 'image/jpeg' });
        
        // Show captured image in preview
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('image-preview');
            preview.src = e.target.result;
        };
        reader.readAsDataURL(imageBlob);
        
        // Predict based on mode
        let response;
        if (currentMode === 'face') {
            response = await predictFace(uploadedImage);
        } else if (currentMode === 'multimodal') {
            const textInput = document.getElementById('text-input').value.trim();
            if (!textInput) {
                showError('Please enter text for multimodal prediction');
                showLoading(false);
                return;
            }
            response = await predictMultimodal(uploadedImage, textInput);
        }
        
        currentPrediction = response;
        displayResults(response);
        loadQTable();
        loadStatistics();
        
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

// Handle mode change
function handleModeChange(mode) {
    currentMode = mode;
    
    // Update button states
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });
    
    // Show/hide sections
    const imageSection = document.getElementById('image-section');
    const textSection = document.getElementById('text-section');
    
    if (mode === 'multimodal') {
        imageSection.style.display = 'block';
        textSection.style.display = 'block';
        // Stop live detection in multimodal mode
        isLiveDetecting = false;
        document.getElementById('live-prediction').style.display = 'none';
    } else if (mode === 'face') {
        imageSection.style.display = 'block';
        textSection.style.display = 'none';
        // Start live detection if camera is active
        if (cameraStream && cameraMode === 'camera') {
            startLiveDetection();
        }
    } else if (mode === 'text') {
        imageSection.style.display = 'none';
        textSection.style.display = 'block';
        // Stop camera if active
        stopCamera();
    }
}

// Handle image upload
function handleImageUpload(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please upload a valid image file');
        return;
    }
    
    uploadedImage = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.getElementById('image-preview');
        preview.src = e.target.result;
        preview.style.display = 'block';
        document.querySelector('.upload-placeholder').style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Handle prediction
async function handlePredict() {
    // Validate inputs
    if ((currentMode === 'multimodal' || currentMode === 'face') && !uploadedImage) {
        showError('Please upload an image');
        return;
    }
    
    const textInput = document.getElementById('text-input').value.trim();
    if ((currentMode === 'multimodal' || currentMode === 'text') && !textInput) {
        showError('Please enter text');
        return;
    }
    
    // Show loading
    showLoading(true);
    
    try {
        let response;
        
        if (currentMode === 'multimodal') {
            response = await predictMultimodal(uploadedImage, textInput);
        } else if (currentMode === 'face') {
            response = await predictFace(uploadedImage);
        } else if (currentMode === 'text') {
            response = await predictText(textInput);
        }
        
        currentPrediction = response;
        displayResults(response);
        loadQTable();
        loadStatistics();
    } catch (error) {
        showError(error.message);
    } finally {
        showLoading(false);
    }
}

// API calls
async function predictMultimodal(image, text) {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('text', text);
    
    const response = await fetch('/api/predict/multimodal', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Prediction failed');
    }
    
    return await response.json();
}

async function predictFace(image) {
    const formData = new FormData();
    
    // Handle both File objects and Blobs
    if (image instanceof Blob && !(image instanceof File)) {
        // Convert Blob to File with proper name
        const file = new File([image], 'camera-capture.jpg', { type: 'image/jpeg' });
        formData.append('image', file);
    } else {
        formData.append('image', image);
    }
    
    const response = await fetch('/api/predict/face', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Prediction failed');
    }
    
    return await response.json();
}

async function predictText(text) {
    const response = await fetch('/api/predict/text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Prediction failed');
    }
    
    return await response.json();
}

// Display results
function displayResults(data) {
    const container = document.getElementById('results-container');
    
    const html = `
        <div class="result-card">
            <div class="result-emotion">${data.emotion.toUpperCase()}</div>
            <div class="result-confidence">
                Confidence: ${(data.confidence * 100).toFixed(1)}%
            </div>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${data.confidence * 100}%"></div>
            </div>
            
            ${data.modality === 'fusion' ? `
                <div class="result-details">
                    <div class="detail-item">
                        <div class="detail-label">Face Prediction</div>
                        <div class="detail-value">${data.face_emotion}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Text Prediction</div>
                        <div class="detail-value">${data.text_emotion}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Fusion Method</div>
                        <div class="detail-value">${data.fusion_method}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">State</div>
                        <div class="detail-value">State ${data.state}</div>
                    </div>
                </div>
            ` : ''}
            
            <div class="probabilities-grid">
                ${Object.entries(data.probabilities).map(([emotion, prob]) => `
                    <div class="prob-item">
                        <div class="prob-label">${emotion}</div>
                        <div class="prob-value">${(prob * 100).toFixed(1)}%</div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Show feedback section
    document.getElementById('feedback-section').style.display = 'block';
    document.getElementById('correction-section').style.display = 'none';
}

// Handle feedback
function handleFeedback(isCorrect) {
    if (isCorrect) {
        submitFeedback(currentPrediction.emotion);
    } else {
        document.getElementById('correction-section').style.display = 'block';
    }
}

// Submit correction
function submitCorrection() {
    const correctEmotion = document.getElementById('correct-emotion').value;
    submitFeedback(correctEmotion);
}

// Submit feedback to server
async function submitFeedback(correctEmotion) {
    if (!currentPrediction) return;
    
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                correct_emotion: correctEmotion,
                predicted_emotion: currentPrediction.emotion,
                state: currentPrediction.state || 0,
                action: currentPrediction.action || 0
            })
        });
        
        if (response.ok) {
            showSuccess('Feedback submitted! Q-table updated.');
            document.getElementById('feedback-section').style.display = 'none';
            loadQTable();
            loadStatistics();
        }
    } catch (error) {
        showError('Failed to submit feedback');
    }
}

// Load Q-table
async function loadQTable() {
    try {
        const response = await fetch('/api/qtable');
        const data = await response.json();
        
        displayQTable(data);
        
        document.getElementById('epsilon-value').textContent = data.epsilon.toFixed(4);
        document.getElementById('episodes-value').textContent = data.episodes;
    } catch (error) {
        console.error('Failed to load Q-table:', error);
    }
}

// Display Q-table
function displayQTable(data) {
    const container = document.getElementById('qtable-container');
    
    const html = `
        <table class="qtable">
            <thead>
                <tr>
                    <th>State</th>
                    ${data.actions.map(action => `<th>${action}</th>`).join('')}
                    <th>Best Action</th>
                </tr>
            </thead>
            <tbody>
                ${data.qtable.map((row, stateIdx) => {
                    const bestActionIdx = row.indexOf(Math.max(...row));
                    return `
                        <tr>
                            <td>${data.states[stateIdx]}</td>
                            ${row.map(val => `<td>${val.toFixed(4)}</td>`).join('')}
                            <td class="best-action">${data.actions[bestActionIdx]}</td>
                        </tr>
                    `;
                }).join('')}
            </tbody>
        </table>
    `;
    
    container.innerHTML = html;
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();
        
        document.getElementById('total-predictions').textContent = data.session.predictions;
        document.getElementById('accuracy').textContent = data.session.accuracy + '%';
        document.getElementById('stat-face').textContent = data.session.face_only;
        document.getElementById('stat-text').textContent = data.session.text_only;
        document.getElementById('stat-fusion').textContent = data.session.fusion;
        document.getElementById('stat-correct').textContent = data.session.correct;
    } catch (error) {
        console.error('Failed to load statistics:', error);
    }
}

// Utility functions
function showLoading(show) {
    document.getElementById('loading-overlay').style.display = show ? 'flex' : 'none';
}

function showError(message) {
    alert('Error: ' + message);
}

function showSuccess(message) {
    alert(message);
}
