document.addEventListener('DOMContentLoaded', () => {
    // Tabs
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.add('hidden'));

            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.remove('hidden');
        });
    });

    // Image Upload Tab
    const uploadForm = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const dropZone = document.getElementById('drop-zone');
    const fileNameDisplay = document.getElementById('file-name');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    // Results
    const resultsArea = document.getElementById('results-area');
    const resultImage = document.getElementById('result-image');
    const extractedText = document.getElementById('extracted-text');
    const objectTags = document.getElementById('object-tags');
    const summaryText = document.getElementById('summary-text');
    const resultAudio = document.getElementById('result-audio');

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        if (e.dataTransfer.files.length) {
            imageInput.files = e.dataTransfer.files;
            updateFileName();
        }
    });

    imageInput.addEventListener('change', updateFileName);

    function updateFileName() {
        if (imageInput.files.length > 0) {
            fileNameDisplay.textContent = imageInput.files[0].name;
            analyzeBtn.disabled = false;
        } else {
            fileNameDisplay.textContent = 'No file selected';
            analyzeBtn.disabled = true;
        }
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!imageInput.files.length) return;

        // UI state: loading
        setLoading(analyzeBtn, true);
        resultsArea.classList.add('hidden');

        const formData = new FormData();
        formData.append('image', imageInput.files[0]);

        try {
            const res = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await res.json();
            
            if (res.ok) {
                // Populate results
                resultImage.src = data.image_url;
                extractedText.textContent = data.text || '(no text detected)';
                
                objectTags.innerHTML = '';
                if (data.objects && data.objects.length > 0) {
                    data.objects.forEach(tag => {
                        const span = document.createElement('span');
                        span.className = 'tag';
                        span.textContent = tag;
                        objectTags.appendChild(span);
                    });
                } else {
                    objectTags.innerHTML = '<span class="tag" style="background: rgba(255,255,255,0.1); color: #ccc;">No objects</span>';
                }

                summaryText.textContent = data.summary;
                
                // Audio
                resultAudio.src = data.audio_url + '?t=' + new Date().getTime(); // cache buster
                
                resultsArea.classList.remove('hidden');
                resultAudio.play().catch(e => console.log('Autoplay prevented:', e));
            } else {
                alert('Error: ' + data.error);
            }
        } catch (err) {
            alert('Failed to connect to the server.');
            console.error(err);
        } finally {
            setLoading(analyzeBtn, false);
        }
    });

    // TTS Tab
    const ttsForm = document.getElementById('tts-form');
    const ttsInput = document.getElementById('tts-input');
    const speakBtn = document.getElementById('speak-btn');
    const ttsResultArea = document.getElementById('tts-result-area');
    const ttsAudio = document.getElementById('tts-audio');

    ttsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = ttsInput.value.trim();
        if (!text) return;

        setLoading(speakBtn, true);
        ttsResultArea.classList.add('hidden');

        try {
            const res = await fetch('/api/speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            const data = await res.json();
            if (res.ok) {
                ttsAudio.src = data.audio_url + '?t=' + new Date().getTime();
                ttsResultArea.classList.remove('hidden');
                ttsAudio.play().catch(e => console.log('Autoplay prevented:', e));
            } else {
                alert('Error: ' + data.error);
            }
        } catch (err) {
            alert('Failed to connect to the server.');
        } finally {
            setLoading(speakBtn, false);
        }
    });

    function setLoading(btn, isLoading) {
        const text = btn.querySelector('.btn-text');
        const loader = btn.querySelector('.loader');
        
        if (isLoading) {
            text.classList.add('hidden');
            loader.classList.remove('hidden');
            btn.disabled = true;
        } else {
            text.classList.remove('hidden');
            loader.classList.add('hidden');
            btn.disabled = false;
        }
    }
});
