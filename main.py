from flask import Flask, jsonify
import time, random
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="18a3a952d929406393c7878171816bdb",
    client_secret="e921387ee3374101924182052ecec00a",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing",
    cache_path="token.txt"


@app.route("/")
def home():
    return "🎵 Spotify Controller Running"


@app.route("/track")
def track_info():
    playback = sp.current_playback()
    if playback and playback['is_playing']:
        item = playback['item']
        return jsonify({
            "name":
            item['name'],
            "artist":
            ", ".join([a['name'] for a in item['artists']]),
            "album":
            item['album']['name']
        })
    return jsonify({"error": "Nothing playing"})


@app.route("/skip")
def skip():
    sp.next_track()
    return jsonify({"status": "skipped"})


# Run this only once manually to start playback
@app.route("/play")
def play():
    playlist_uri = "spotify:playlist:0fR3oYjLFLjpk5weO1jcLh"
    devices = sp.devices()['devices']
    if devices:
        sp.start_playback(device_id=devices[0]['id'], context_uri=playlist_uri)
        return jsonify({"status": "started"})
    return jsonify({"error": "No device found"})


app.run(host="0.0.0.0", port=3000)
