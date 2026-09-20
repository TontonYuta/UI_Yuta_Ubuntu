#!/usr/bin/env python3
"""
music_engine.py - Advanced MPRIS Music Metadata & Synced Lyrics Engine
Fetches real-time playback, LRCLIB synced lyrics, and album art.
"""

import sys
import os
import time
import re
import json
import urllib.request
import urllib.parse
import subprocess

CACHE_DIR = os.path.expanduser("~/.cache/desktop_lyrics")
ART_CACHE = os.path.expanduser("~/.cache/current_album_art.png")
STATE_FILE = "/tmp/desktop_music.json"

os.makedirs(CACHE_DIR, exist_ok=True)

class MusicEngine:
    def __init__(self):
        self.last_track_id = ""
        self.cached_lyrics = [] # list of (seconds, text)
        self.has_synced = False
        self.last_art_url = ""
        self.manual_pos = 0
        self.last_pos_update = 0

    def clean_title(self, raw_title):
        if not raw_title:
            return ""
        # Remove common noise in youtube titles: (Official MV), [Audio], [MV 4K], etc.
        t = re.sub(r'[\(\[\{].*?(official|audio|mv|video|lyrics|remix|hd|4k|vietsub|cover|tik\s*tok).*?[\)\]\}]', '', raw_title, flags=re.IGNORECASE)
        t = re.sub(r'\s*\|\s*.*$', '', t)
        t = re.sub(r'\s*-\s*.*MV.*$', '', t, flags=re.IGNORECASE)
        return t.strip()

    def get_mpris_data(self):
        try:
            out = subprocess.check_output(['busctl', '--user', 'list'], stderr=subprocess.DEVNULL).decode()
            players = [l.split()[0] for l in out.splitlines() if 'org.mpris.MediaPlayer2' in l]
            if not players:
                return None
            
            # Prioritize players that are currently 'Playing'
            target = players[0]
            playing_target = None
            for p in players:
                try:
                    s_raw = subprocess.check_output(['busctl', '--user', 'get-property', p, '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player', 'PlaybackStatus'], stderr=subprocess.DEVNULL).decode().strip()
                    if 'Playing' in s_raw:
                        playing_target = p
                        break
                except Exception:
                    pass
            if playing_target:
                target = playing_target

            # Status
            status_raw = subprocess.check_output(['busctl', '--user', 'get-property', target, '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player', 'PlaybackStatus'], stderr=subprocess.DEVNULL).decode().strip()
            status = status_raw.split()[-1].replace('\"', '')

            # Position
            pos = 0.0
            try:
                pos_raw = subprocess.check_output(['busctl', '--user', 'get-property', target, '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player', 'Position'], stderr=subprocess.DEVNULL).decode().strip()
                pos = float(pos_raw.split()[-1]) / 1000000.0
            except Exception:
                pass

            # Metadata
            meta_raw = subprocess.check_output(['busctl', '--user', 'get-property', target, '/org/mpris/MediaPlayer2', 'org.mpris.MediaPlayer2.Player', 'Metadata'], stderr=subprocess.DEVNULL).decode()
            title = ''
            artist = ''
            album = ''
            art_url = ''
            length = 0.0

            for line in meta_raw.splitlines():
                if 'xesam:title' in line:
                    parts = line.split('\"')
                    if len(parts) >= 2: title = parts[1]
                elif 'xesam:artist' in line:
                    parts = line.split('\"')
                    if len(parts) >= 2: artist = parts[1]
                elif 'xesam:album' in line:
                    parts = line.split('\"')
                    if len(parts) >= 2: album = parts[1]
                elif 'mpris:artUrl' in line:
                    parts = line.split('\"')
                    if len(parts) >= 2: art_url = parts[1]
                elif 'mpris:length' in line:
                    try:
                        length = float(line.split()[-1]) / 1000000.0
                    except Exception:
                        pass

            if not title or title == 'mpris:trackid':
                return None

            return {
                'player': target,
                'status': status,
                'title': title,
                'artist': artist,
                'album': album,
                'art_url': art_url,
                'pos': pos,
                'len': length
            }
        except Exception:
            return None

    def fetch_lyrics(self, title, artist):
        clean_t = self.clean_title(title)
        cache_key = re.sub(r'[^a-zA-Z0-9]', '_', f"{artist}_{clean_t}").lower()
        cache_file = os.path.join(CACHE_DIR, f"{cache_key}.lrc")

        # Check local cache
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return self.parse_lrc(f.read())
            except Exception:
                pass

        # Query LRCLIB search
        try:
            q = f"{clean_t} {artist}".strip()
            url = f"https://lrclib.net/api/search?q={urllib.parse.quote(q)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'AestheticDesktopMusic/2.0'})
            with urllib.request.urlopen(req, timeout=4) as resp:
                results = json.loads(resp.read().decode('utf-8'))
                if results and isinstance(results, list):
                    best = results[0]
                    synced = best.get("syncedLyrics", "")
                    if synced:
                        with open(cache_file, "w", encoding="utf-8") as f:
                            f.write(synced)
                        return self.parse_lrc(synced)
                    plain = best.get("plainLyrics", "")
                    if plain:
                        return self.parse_plain(plain)
        except Exception:
            pass

        return []

    def parse_lrc(self, lrc_text):
        entries = []
        for line in lrc_text.splitlines():
            matches = re.findall(r'\[(\d+):(\d+(?:\.\d+)?)\]', line)
            if matches:
                text = re.sub(r'\[\d+:\d+(?:\.\d+)?\]', '', line).strip()
                for m in matches:
                    mins = int(m[0])
                    secs = float(m[1])
                    total_sec = mins * 60 + secs
                    if text:
                        entries.append((total_sec, text))
        entries.sort(key=lambda x: x[0])
        self.has_synced = len(entries) > 0
        return entries

    def parse_plain(self, plain_text):
        lines = [l.strip() for l in plain_text.splitlines() if l.strip()]
        self.has_synced = False
        return [(0, l) for l in lines]

    def download_album_art(self, art_url):
        if not art_url or art_url == self.last_art_url:
            return
        self.last_art_url = art_url
        try:
            if art_url.startswith("file://"):
                local_path = urllib.parse.unquote(art_url[7:])
                if os.path.exists(local_path):
                    import shutil
                    shutil.copy(local_path, ART_CACHE)
            elif art_url.startswith("http://") or art_url.startswith("https://"):
                req = urllib.request.Request(art_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    with open(ART_CACHE, "wb") as f:
                        f.write(resp.read())
        except Exception:
            pass

    def get_current_lyrics(self, current_pos):
        if not self.cached_lyrics:
            return "", ""
        if not self.has_synced:
            # Return first line or rotate
            return self.cached_lyrics[0][1] if self.cached_lyrics else "", ""

        cur = ""
        nxt = ""
        for i, (ts, text) in enumerate(self.cached_lyrics):
            if current_pos >= ts:
                cur = text
                if i + 1 < len(self.cached_lyrics):
                    nxt = self.cached_lyrics[i + 1][1]
                else:
                    nxt = ""
            else:
                break
        return cur, nxt

    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def update_state(self):
        data = self.get_mpris_data()
        if not data or data['status'] == 'Stopped':
            empty_state = {
                "active": False,
                "status": "Stopped",
                "title": "",
                "artist": "",
                "album": "",
                "pos_str": "00:00",
                "len_str": "00:00",
                "progress_percent": 0.0,
                "progress_bar": "──────────────",
                "current_lyric": "Chưa có bài hát nào đang phát",
                "next_lyric": "",
                "has_lyrics": False,
                "art_path": ART_CACHE if os.path.exists(ART_CACHE) else "",
                "updated_at": time.time()
            }
            self.write_state(empty_state)
            return empty_state

        track_id = f"{data['artist']}_{data['title']}"
        if track_id != self.last_track_id:
            self.last_track_id = track_id
            self.cached_lyrics = self.fetch_lyrics(data['title'], data['artist'])
            self.download_album_art(data['art_url'])

        pos = data['pos']
        length = data['len']
        pct = (pos / length * 100.0) if length > 0 else 0.0

        # Build ASCII progress bar
        total_chars = 14
        filled = int(round(pct / 100.0 * total_chars)) if length > 0 else 0
        p_bar = "═" * filled + "─" * (total_chars - filled)

        cur_lyric, nxt_lyric = self.get_current_lyrics(pos)
        if not cur_lyric and not self.cached_lyrics:
            cur_lyric = f"{data['title']} - {data['artist']}" if data['artist'] else data['title']

        state = {
            "active": True,
            "status": data['status'],
            "title": data['title'],
            "artist": data['artist'],
            "album": data['album'],
            "pos": pos,
            "len": length,
            "pos_str": self.format_time(pos),
            "len_str": self.format_time(length),
            "progress_percent": round(pct, 1),
            "progress_bar": p_bar,
            "current_lyric": cur_lyric,
            "next_lyric": nxt_lyric,
            "has_lyrics": len(self.cached_lyrics) > 0,
            "art_path": ART_CACHE if os.path.exists(ART_CACHE) else "",
            "updated_at": time.time()
        }
        self.write_state(state)
        return state

    def write_state(self, state):
        try:
            tmp = STATE_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            os.replace(tmp, STATE_FILE)
        except Exception:
            pass

    def run_daemon(self):
        while True:
            self.update_state()
            time.sleep(0.25)

def main():
    engine = MusicEngine()
    arg = sys.argv[1] if len(sys.argv) > 1 else "--update"

    if arg == "--daemon":
        engine.run_daemon()
    else:
        state = engine.update_state()
        if arg == "--lyric":
            print(state.get("current_lyric", ""))
        elif arg == "--next-lyric":
            print(state.get("next_lyric", ""))
        elif arg == "--track":
            t = state.get("title", "")
            a = state.get("artist", "")
            print(f"{t} - {a}" if a else t)
        elif arg == "--progress":
            print(f"{state.get('pos_str', '00:00')} [{state.get('progress_bar', '')}] {state.get('len_str', '00:00')}")
        elif arg == "--json":
            print(json.dumps(state, ensure_ascii=False, indent=2))
        else:
            print(state.get("current_lyric", ""))

if __name__ == "__main__":
    main()
