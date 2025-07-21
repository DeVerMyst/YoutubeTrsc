import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import timedelta
import re

st.set_page_config(page_title="YouTube Transcript Search", layout="wide")
st.title("🎬 YouTube Transcript Timestamp Finder")

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))  # Ex: '0:01:32'

# Champ d’entrée
url = st.text_input("🎯 Collez ici l'URL d'une vidéo YouTube avec sous-titres activés :")

if url:
    video_id = extract_video_id(url)
    if video_id:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr', 'en','pl'])
            st.success(f"Transcription trouvée ! ({len(transcript)} lignes)")
            selected_line = st.radio(
                "📝 Cliquez une phrase pour voir son timestamp :",
                options=[f"[{format_time(t['start'])}] {t['text']}" for t in transcript],
                index=0
            )

            if selected_line:
                # Extraire le temps
                match = re.match(r"\[(\d+:\d+:\d+)\]", selected_line)
                if match:
                    h, m, s = map(int, match.group(1).split(":"))
                    total_seconds = h * 3600 + m * 60 + s
                    yt_link = f"https://www.youtube.com/watch?v={video_id}&t={total_seconds}s"
                    st.info(f"⏱ Cette phrase commence à `{match.group(1)}`")
                    st.markdown(f"[▶️ Ouvrir sur YouTube à ce moment précis]({yt_link})", unsafe_allow_html=True)



        except Exception as e:
            st.error(f"Erreur lors de la récupération de la transcription :\n{e}")
    else:
        st.warning("Impossible d'extraire l'ID de la vidéo. Vérifie l'URL.")
