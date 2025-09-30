from __future__ import annotations
import os, time
from dotenv import load_dotenv
import streamlit as st
from tqdm import tqdm
from scrape import extract_from_url
from llm import blog_to_podcast_json
# Use Windows-compatible TTS module to avoid ffmpeg issues
from tts_windows import synth_ssml_to_mp3_segments, join_segments_to_podcast

load_dotenv()

st.set_page_config(page_title="AI Blog → Podcast", page_icon="🎙️", layout="centered")
st.title("🎙️ Blog → Podcast ")

tab1, tab2 = st.tabs(["From URL", "Paste Text"])

article_text = ""
with tab1:
    url = st.text_input("Blog URL")
    if st.button("Fetch"):
        with st.spinner("Extracting…"):
            try:
                article_text = extract_from_url(url)
                st.success(f"Extracted {len(article_text)} chars")
                st.session_state["article_text"] = article_text
            except Exception as e:
                st.error(f"Failed to extract: {e}")

with tab2:
    pasted = st.text_area("Paste article text", height=240)
    if st.button("Use this text"):
        article_text = pasted
        st.session_state["article_text"] = article_text

article_text = st.session_state.get("article_text", "")

if article_text:
    st.subheader("Article preview")
    st.write(article_text[:1500] + ("…" if len(article_text) > 1500 else ""))

    if st.button("Ask Claude to Draft Podcast (Outline + SSML)"):
        with st.spinner("Asking Claude…"):
            try:
                data = blog_to_podcast_json(article_text)
                st.session_state["podcast_plan"] = data
                st.success("Got outline & SSML from Claude.")
            except Exception as e:
                st.error(f"Claude error: {e}")

plan = st.session_state.get("podcast_plan")
if plan:
    st.subheader("Planned Episode")
    st.markdown(f"**Title:** {plan.get('title','')}")
    st.markdown(f"**Hook:** {plan.get('hook','')}")
    st.markdown("**Sections:**")
    for s in plan.get("sections", []):
        st.markdown(f"- {s}")
    st.markdown(f"**CTA:** {plan.get('cta','')}")

    with st.expander("SSML Segments (preview)"):
        for seg in plan["segments"]:
            st.code(seg["ssml"], language="xml")

    voice_id = st.text_input("ElevenLabs Voice ID", os.environ.get("ELEVEN_LABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"))
    out_dir = "audio/segments"
    final_mp3 = "audio/podcast.mp3"

    if st.button("Synthesize & Join"):
        try:
            with st.spinner("Generating audio segments (this may take a few minutes)..."):
                paths = synth_ssml_to_mp3_segments(plan["segments"], out_dir, voice_id=voice_id)

            if not paths:
                st.error("No audio segments were generated. Please check your ElevenLabs API key.")
                st.stop()

            st.info(f"Successfully generated {len(paths)} audio segments!")

            with st.spinner("Joining segments into final podcast..."):
                out = join_segments_to_podcast(paths, final_mp3)

            st.success(f"✅ Podcast created successfully: {out}")
            st.info("💡 Using Windows-compatible audio processing. For professional audio quality, install ffmpeg.")

            try:
                with open(out, "rb") as f:
                    st.download_button("⬇️ Download podcast.mp3", f, file_name="podcast.mp3", mime="audio/mpeg")
            except FileNotFoundError:
                st.error(f"Could not find the generated file: {out}")

        except Exception as e:
            st.error(f"❌ TTS error: {e}")
            st.info("💡 Tip: Make sure your ELEVEN_LABS_API_KEY is valid and you have internet connection.")
