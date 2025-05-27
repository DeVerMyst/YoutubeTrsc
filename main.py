import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="YouTube Transcript Finder", layout="wide")
st.title("📺 YouTube Transcript Explorer")

# Input de l'URL
url = st.text_input("Entrez une URL YouTube :", placeholder="https://www.youtube.com/watch?v=...")

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

if url:
    video_id = extract_video_id(url)
    if video_id:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr', 'en','pl'])
            
            st.subheader("🔎 Transcription")
            selected_line = st.radio(
                "Clique une phrase pour voir le timecode :",
                options=[f"[{round(t['start'],1)}s] {t['text']}" for t in transcript],
                index=0
            )
            
            # Affiche le timestamp sélectionné
            if selected_line:
                match = re.match(r"\[(\d+\.?\d*)s\]", selected_line)
                if match:
                    start_time = float(match.group(1))
                    st.info(f"⏱ Cette phrase commence à **{start_time} secondes**.")
                    video_link = f"https://www.youtube.com/watch?v={video_id}&t={int(start_time)}s"
                    st.markdown(f"[▶️ Aller à ce moment dans la vidéo]({video_link})", unsafe_allow_html=True)

            # Bloc texte pour Ctrl+F
            st.markdown("---")
            st.text_area(
                label="🧾 Texte complet (Ctrl+F possible)",
                value="\n".join([f"[{round(t['start'],1)}s] {t['text']}" for t in transcript]),
                height=400
            )
        except Exception as e:
            st.error(f"Erreur lors de la récupération : {e}")
    else:
        st.warning("Impossible d’extraire l’ID de la vidéo. Vérifie l’URL.")
