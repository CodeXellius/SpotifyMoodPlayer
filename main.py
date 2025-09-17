import cv2
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import webbrowser
from collections import deque
from statistics import mode, StatisticsError

# -------------------- Spotify Setup --------------------
SPOTIPY_CLIENT_ID = 'YOUR_SPOTIPY_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'YOUR_SPOTIPY_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

scope = "user-modify-playback-state user-read-playback-state user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))

# -------------------- Mood to Playlist Mapping --------------------
playlist_dict = {
    "happy": "https://open.spotify.com/playlist/5dXAx2SUT0MUdWLKwcUBr3?si=392962895d35438d",
    "sad": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1?si=3f6e2f3f4f6b4e1e",
    "neutral": "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF?si=6a11d63de24c43b7",
    "angry": "https://open.spotify.com/playlist/0cj48sijCRDJ3Hatx1k1vJ?si=S7T0f3X8Sg-sGScS0ldZgA",
}

# -------------------- Webcam Setup --------------------
cap = cv2.VideoCapture(0)
time.sleep(2)
print("Detecting your mood silently for 3 seconds...")

# Store detected emotions for smoothing
recent_emotions = deque(maxlen=30)  # ~3 seconds at ~10 fps

start_time = time.time()
detection_duration = 3  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    try:
        # Analyze emotion
        result = DeepFace.analyze(small_frame, actions=['emotion'], enforce_detection=False)
        if isinstance(result, list):
            result = result[0]

        dominant_emotion = result['dominant_emotion']
        recent_emotions.append(dominant_emotion)

    except Exception as e:
        # Ignore errors, continue silently
        continue

    # Stop after detection_duration seconds
    if time.time() - start_time > detection_duration:
        break

cap.release()

# Determine the most frequent emotion detected
try:
    final_emotion = mode(recent_emotions)
except StatisticsError:
    final_emotion = recent_emotions[-1] if recent_emotions else "neutral"

print(f"\nFinal Detected Mood: {final_emotion}")

# Play playlist based on final emotion
if final_emotion in playlist_dict:
    playlist_uri = playlist_dict[final_emotion]
    print(f"Playing playlist for {final_emotion} mood...")

    try:
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            sp.start_playback(device_id=device_id, context_uri=playlist_uri)
            print("Playing on your Spotify device...")
        else:
            print("No active Spotify device found. Opening in web browser...")
            webbrowser.open(playlist_uri)

    except spotipy.exceptions.SpotifyException:
        print("Cannot play directly (Free account?). Opening in web browser...")
        webbrowser.open(playlist_uri)
