const { spawn } = require('child_process');
const path = require('path');
const crypto = require('crypto');
const fs = require('fs');

// Ensure uploads and outputs directories exist
const uploadsDir = path.join(__dirname, '..', 'uploads');
const outputsDir = path.join(__dirname, '..', 'outputs');
if (!fs.existsSync(uploadsDir)) fs.mkdirSync(uploadsDir);
if (!fs.existsSync(outputsDir)) fs.mkdirSync(outputsDir);

exports.analyzeImage = (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No image provided' });
  }

  const imagePath = req.file.path;
  const uniqueId = crypto.randomBytes(4).toString('hex');
  const outImgName = `det_${uniqueId}_${req.file.filename}`;
  const outImgPath = path.join(__dirname, '..', 'outputs', outImgName);
  
  // Call the Python script
  const pythonProcess = spawn('python', [
    path.join(__dirname, '..', 'ai_runner.py'),
    '--image', imagePath,
    '--out_img_path', outImgPath
  ]);

  let stdoutData = '';
  let stderrData = '';

  pythonProcess.stdout.on('data', (data) => {
    stdoutData += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    stderrData += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python process exited with code ${code}`);
      console.error(stderrData);
      return res.status(500).json({ error: 'Internal server error during analysis' });
    }

    try {
      const result = JSON.parse(stdoutData.trim());
      if (result.success) {
        // Run TTS generation as a separate step for the summary
        const audioName = `audio_${uniqueId}.mp3`;
        const audioPath = path.join(__dirname, '..', 'outputs', audioName);
        
        const ttsProcess = spawn('python', [
          path.join(__dirname, '..', 'tts_runner.py'),
          '--text', result.summary,
          '--out_audio_path', audioPath
        ]);

        ttsProcess.on('close', (ttsCode) => {
          res.json({
            text: result.text,
            objects: result.objects,
            summary: result.summary,
            image_url: `/outputs/${outImgName}`,
            audio_url: `/outputs/${audioName}`
          });
        });
      } else {
        res.status(500).json({ error: result.error });
      }
    } catch (e) {
      console.error('Failed to parse Python JSON output:', e);
      console.error('Output was:', stdoutData);
      res.status(500).json({ error: 'Failed to parse analysis result' });
    }
  });
};

exports.generateSpeech = (req, res) => {
  const { text } = req.body;
  if (!text) {
    return res.status(400).json({ error: 'No text provided' });
  }

  const uniqueId = crypto.randomBytes(4).toString('hex');
  const audioName = `speak_${uniqueId}.mp3`;
  const audioPath = path.join(__dirname, '..', 'outputs', audioName);

  const ttsProcess = spawn('python', [
    path.join(__dirname, '..', 'tts_runner.py'),
    '--text', text,
    '--out_audio_path', audioPath
  ]);

  let stdoutData = '';

  ttsProcess.stdout.on('data', (data) => {
    stdoutData += data.toString();
  });

  ttsProcess.on('close', (code) => {
    try {
      const result = JSON.parse(stdoutData.trim());
      if (result.success) {
        res.json({ audio_url: `/outputs/${audioName}` });
      } else {
        res.status(500).json({ error: result.error || 'Failed to generate audio' });
      }
    } catch (e) {
      console.error('Failed to parse TTS JSON output:', e);
      res.status(500).json({ error: 'Failed to generate audio' });
    }
  });
};
