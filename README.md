# Video Audio Amplifier 🎵

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A powerful desktop application for amplifying audio in video files with a user-friendly interface. Built with Python using a clean architecture pattern.

## 🎯 Features

- 📊 Real-time progress tracking
- 🎚️ Adjustable amplification factor
- 🎥 Support for multiple video formats
- 📁 Intuitive file selection interface
- 🧰 Clean architecture with separated backend/frontend
- 🔄 Non-blocking UI during processing

## 📋 Requirements

- Python 3.8+
- MoviePy
- PyDub
- Tkinter (usually comes with Python)

## 🚀 Installation

1. Clone the repository
```bash
git clone https://github.com/archibald-carrion/Video-audio-amplifier.git
cd Video-audio-amplifier
```

2. Install required packages
```bash
pip install moviepy pydub
```

## 🎮 Usage

Run the application:
```bash
python main.py
```

### Step-by-step guide:

1. Click "Browse" to select an input video file
2. Choose output location (auto-suggested with '_amplified' suffix)
3. Adjust amplification factor (default: 2.0)
4. Click "Process Video" to start
5. Monitor progress through the progress bar
