# MoodPlayer 🎵

MoodPlayer uses your webcam and AI to detect your mood, then plays a matching Spotify playlist automatically!

## Features

- Detects your mood (`happy`, `sad`, `neutral`, `angry`) using DeepFace.
- Plays a Spotify playlist that matches your mood.
- Works with your active Spotify device, or opens the playlist in your browser.

## Requirements

- Python 3.8+
- Webcam
- Spotify account (Premium recommended for direct playback)
- The following Python packages:
  - opencv-python
  - deepface
  - spotipy
  - tf-keras
  - tensorflow

## Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/MoodPlayer.git
   cd MoodPlayer
   ```

2. **Create a virtual environment:**
   ```
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up Spotify Developer credentials:**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
   - Create an app and get your `Client ID` and `Client Secret`.
   - Replace them in `main.py`:
     ```python
     SPOTIPY_CLIENT_ID = 'your_client_id'
     SPOTIPY_CLIENT_SECRET = 'your_client_secret'
     ```

## Usage

1. **Run the program:**
   ```
   python main.py
   ```

2. **Look at your webcam for 3 seconds.**
3. **Enjoy music that matches your mood!**

## Notes

- If no Spotify device is active, the playlist will open in your browser. You must click "Play" manually.
- For best results, use Spotify Premium.

## License

MIT License
