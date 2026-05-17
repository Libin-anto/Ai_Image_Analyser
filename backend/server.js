require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const analyzeRoutes = require('./routes/analyzeRoutes');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Serve outputs statically so frontend can access images and audio
app.use('/outputs', express.static(path.join(__dirname, 'outputs')));

// Routes
app.use('/api', analyzeRoutes);

app.listen(PORT, () => {
  console.log(`Node.js Backend server running on port ${PORT}`);
});
