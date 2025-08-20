import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import os
from tkinter import messagebox
import subprocess
import platform
import glob

def visualize_logs():
    log_dir = os.path.abspath("logs")
    os.makedirs(log_dir, exist_ok=True)

    # Get list of session folders
    sessions = sorted(
        glob.glob(os.path.join(log_dir, "session_*")),
        key=os.path.getmtime,
        reverse=True
    )

    if not sessions:
        messagebox.showinfo("Info", "No session logs found.")
        return

    latest_session = sessions[0]
    print(f"[INFO] Using session: {latest_session}")

    # Find the raw CSV inside the latest session folder
    raw_files = glob.glob(os.path.join(latest_session, "raw_emotion_log_*.csv"))
    if not raw_files:
        messagebox.showerror("Error", "No raw emotion log found in the latest session.")
        return

    raw_csv = raw_files[0]
    output_csv = raw_csv.replace(".csv", "_smoothed.csv")

    try:
        process_emotion_csv(raw_csv, output_csv)

        # Open the folder directly
        system = platform.system()
        if system == "Windows":
            subprocess.run(["explorer", latest_session])
        elif system == "Darwin":
            subprocess.run(["open", latest_session])
        else:
            subprocess.run(["xdg-open", latest_session])
    except Exception as e:
        messagebox.showerror("Error", f"Could not visualize logs:\n{e}")

def process_emotion_csv(input_csv, output_csv, window_size=25):
    if not os.path.exists(input_csv):
        print(f"[PROCESS] File not found: {input_csv}")
        return

    df = pd.read_csv(input_csv)
    if df.empty:
        print("[PROCESS] CSV is empty. Skipping processing.")
        return

    if 'dominant_emotion' not in df.columns:
        print("[PROCESS] 'dominant_emotion' column not found. Skipping.")
        return

    emotions = df['dominant_emotion'].tolist()
    timestamps = df['timestamp'].tolist()

    smoothed = []
    for i in range(len(emotions)):
        window = emotions[max(0, i - window_size + 1): i + 1]
        mode = Counter(window).most_common(1)[0][0]
        smoothed.append((timestamps[i], mode))

    out_df = pd.DataFrame(smoothed, columns=['timestamp', 'smoothed_emotion'])
    out_df.to_csv(output_csv, index=False)
    print(f"[PROCESS] Smoothed emotion log saved to {output_csv}")

    session_dir = os.path.dirname(output_csv)
    base_name = os.path.splitext(os.path.basename(output_csv))[0]
    plot_bar_chart(out_df, os.path.join(session_dir, f"{base_name}_distribution.png"))
    plot_time_series(out_df, os.path.join(session_dir, f"{base_name}_timeline.png"))

def plot_bar_chart(df, output_img_path):
    emotion_counts = df['smoothed_emotion'].value_counts().sort_values(ascending=True)

    plt.figure(figsize=(8, 5))
    emotion_counts.plot(kind='barh', color='skyblue')
    plt.title("Overall Smoothed Emotion Distribution")
    plt.xlabel("Count")
    plt.ylabel("Emotion")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_img_path)
    plt.close()

    print(f"[PLOT] Bar chart saved: {output_img_path}")

def plot_time_series(df, output_img_path):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')

    emotion_levels = {emotion: i for i, emotion in enumerate(df['smoothed_emotion'].unique())}
    reverse_levels = {v: k for k, v in emotion_levels.items()}
    df['emotion_id'] = df['smoothed_emotion'].map(emotion_levels)

    plt.figure(figsize=(12, 5))
    plt.scatter(df['timestamp'], df['emotion_id'], color='purple', s=30)
    plt.yticks(list(reverse_levels.keys()), list(reverse_levels.values()))
    plt.xticks(rotation=45)
    plt.title("Smoothed Emotion Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Emotion")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(output_img_path)
    plt.close()

    print(f"[PLOT] Timeline scatter plot saved: {output_img_path}")