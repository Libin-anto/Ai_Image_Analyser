const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const analyzeController = require('../controllers/analyzeController');

// Multer setup for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + path.extname(file.originalname));
  }
});
const upload = multer({ storage: storage });

router.post('/analyze', upload.single('image'), analyzeController.analyzeImage);
router.post('/speak', analyzeController.generateSpeech);

module.exports = router;
