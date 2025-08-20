# Emoji Cam

This project is a real-time facial emotion recognition system with a GUI pipeline built using OpenCV, FER, and modular utility scripts.

## Features

- Emotion detection using FER
- Real-time webcam display
- Emoji overlay based on detected emotions
- Logging to CSV for emotion data

## Folder Structure

```
├── camera_utils.py
├── config.json
├── csv_logger.py
├── emoji_utils.py
├── emojis
│   ├── angry.png
│   ├── disgust.png
│   ├── fear.png
│   ├── happy.png
│   ├── neutral.png
│   ├── sad.png
│   └── surprised.png
├── fer_pipeline.py
├── main.py
├── models
│   └── mtcnn
│       ├── onet.pt
│       ├── pnet.pt
│       └── rnet.pt
├── process_emotion.py
├── README.md
├── requirements.txt
├── settings.py
└── visual_utils.py
```

## How to Run

Use Python 3.11 when setting up a Virtual Environment

If using Mac, run the following command. Required to ensure Tkinter (GUI) is included
```bash
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m venv venv
```

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## CSV Logging

If `logging_toggle` is enabled in `config.json`, the app logs emotion scores over time into a CSV file via `csv_logger.py`.

- Applies **sliding window mode smoothing** to reduce noise in emotion predictions.
   - Look back at the last `25` emotions.
   - Count which emotion appears most often (the **mode**).
   - Assign that as the smoothed emotion for the current timestamp.

This reduces jitter and makes trends more reliable.

- A **bar chart** of overall emotion distribution
- A **timeline scatter plot** showing emotion changes over time
