from __future__ import annotations
import os
from dotenv import load_dotenv
import streamlit as st
from agents import PodcastOrchestrator

load_dotenv()

st.set_page_config(page_title="AI Blog → Podcast (Agentic)", page_icon="🎙️", layout="centered")
st.title("🎙️ Blog → Podcast (Agentic Architecture)")

st.info("ℹ️ This version uses a multi-agent architecture with specialized agents coordinated by an orchestrator.")

# Display agent architecture
with st.expander("🤖 View Agent Architecture"):
    st.markdown("""
    ### Multi-Agent Pipeline

    **Orchestrator** coordinates these specialized agents:

    1. **🌐 Web Scraper Agent** - Extracts clean content from URLs
    2. **🔍 Content Analyzer Agent** - Analyzes structure and insights
    3. **📝 SSML Specialist Agent** - Generates optimized SSML
    4. **🎵 Audio Producer Agent** - Creates final podcast audio

    Each agent has specific responsibilities and communicates through structured data.
    """)

# Initialize orchestrator
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = PodcastOrchestrator()

tab1, tab2 = st.tabs(["From URL (Full Pipeline)", "From Text (Skip Web Scraper)"])

# Tab 1: URL to Podcast (all agents)
with tab1:
    st.subheader("🌐 Full Agentic Pipeline")
    url = st.text_input("Blog URL", key="url_input")
    voice_id = st.text_input("ElevenLabs Voice ID",
                             os.environ.get("ELEVEN_LABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
                             key="voice_url")

    if st.button("🚀 Run Complete Pipeline", key="run_url"):
        if not url:
            st.error("Please enter a URL")
        else:
            # Create progress tracking
            progress_container = st.container()
            log_container = st.expander("📋 Agent Execution Log", expanded=True)

            with progress_container:
                progress = st.progress(0)
                status = st.empty()

                # Step 1: Web Scraper
                status.text("🌐 Web Scraper Agent: Extracting content...")
                progress.progress(25)

                # Step 2: Content Analyzer
                status.text("🔍 Content Analyzer Agent: Analyzing structure...")
                progress.progress(40)

                # Step 3: SSML Specialist
                status.text("📝 SSML Specialist Agent: Generating SSML...")
                progress.progress(60)

                # Step 4: Audio Producer
                status.text("🎵 Audio Producer Agent: Creating audio...")
                progress.progress(80)

                # Run orchestrator
                result = st.session_state.orchestrator.from_url(
                    url=url,
                    voice_id=voice_id,
                    out_dir="audio/segments",
                    final_mp3="audio/podcast.mp3"
                )

                progress.progress(100)
                status.text("✅ Pipeline complete!")

            # Display execution log
            with log_container:
                for log_entry in result["execution_log"]:
                    icon = "✅" if log_entry["success"] else "❌"
                    st.text(f"{icon} {log_entry['agent']}: {log_entry['step']}")
                    if log_entry.get("error"):
                        st.error(f"   Error: {log_entry['error']}")

            # Handle result
            if result["success"]:
                st.success("🎉 Podcast created successfully!")

                data = result["data"]

                # Display results
                st.subheader("📊 Agent Results")

                # Scraper results
                with st.expander("🌐 Web Scraper Results"):
                    st.json(data["scraper"])

                # Analyzer results
                with st.expander("🔍 Content Analysis"):
                    st.json(data["analysis"])

                # Podcast plan
                plan = data["podcast_plan"]
                st.subheader("🎙️ Planned Episode")
                st.markdown(f"**Title:** {plan.get('title','')}")
                st.markdown(f"**Hook:** {plan.get('hook','')}")
                st.markdown("**Sections:**")
                for s in plan.get("sections", []):
                    st.markdown(f"- {s}")
                st.markdown(f"**CTA:** {plan.get('cta','')}")

                with st.expander("📝 SSML Segments"):
                    for seg in plan["segments"]:
                        st.code(seg["ssml"], language="xml")

                # Audio results
                with st.expander("🎵 Audio Production Results"):
                    st.json(data["audio"])

                # Download button
                final_file = data["audio"]["final_podcast"]
                try:
                    with open(final_file, "rb") as f:
                        st.download_button(
                            "⬇️ Download podcast.mp3",
                            f,
                            file_name="podcast.mp3",
                            mime="audio/mpeg"
                        )
                except FileNotFoundError:
                    st.error(f"Could not find the generated file: {final_file}")
            else:
                st.error(f"❌ Pipeline failed: {result.get('error', 'Unknown error')}")

# Tab 2: Text to Podcast (skip web scraper)
with tab2:
    st.subheader("📝 Text-Based Pipeline")
    st.info("This skips the Web Scraper agent and starts directly with Content Analyzer.")

    text = st.text_area("Paste article text", height=240, key="text_input")
    voice_id_text = st.text_input("ElevenLabs Voice ID",
                                   os.environ.get("ELEVEN_LABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
                                   key="voice_text")

    if st.button("🚀 Run Pipeline (Skip Web Scraper)", key="run_text"):
        if not text:
            st.error("Please paste some text")
        else:
            # Create progress tracking
            progress_container = st.container()
            log_container = st.expander("📋 Agent Execution Log", expanded=True)

            with progress_container:
                progress = st.progress(0)
                status = st.empty()

                # Step 1: Content Analyzer
                status.text("🔍 Content Analyzer Agent: Analyzing structure...")
                progress.progress(33)

                # Step 2: SSML Specialist
                status.text("📝 SSML Specialist Agent: Generating SSML...")
                progress.progress(66)

                # Step 3: Audio Producer
                status.text("🎵 Audio Producer Agent: Creating audio...")
                progress.progress(90)

                # Run orchestrator
                result = st.session_state.orchestrator.from_text(
                    text=text,
                    voice_id=voice_id_text,
                    out_dir="audio/segments",
                    final_mp3="audio/podcast.mp3"
                )

                progress.progress(100)
                status.text("✅ Pipeline complete!")

            # Display execution log
            with log_container:
                for log_entry in result["execution_log"]:
                    icon = "✅" if log_entry["success"] else "❌"
                    st.text(f"{icon} {log_entry['agent']}: {log_entry['step']}")
                    if log_entry.get("error"):
                        st.error(f"   Error: {log_entry['error']}")

            # Handle result
            if result["success"]:
                st.success("🎉 Podcast created successfully!")

                data = result["data"]

                # Display results
                st.subheader("📊 Agent Results")

                # Analyzer results
                with st.expander("🔍 Content Analysis"):
                    st.json(data["analysis"])

                # Podcast plan
                plan = data["podcast_plan"]
                st.subheader("🎙️ Planned Episode")
                st.markdown(f"**Title:** {plan.get('title','')}")
                st.markdown(f"**Hook:** {plan.get('hook','')}")
                st.markdown("**Sections:**")
                for s in plan.get("sections", []):
                    st.markdown(f"- {s}")
                st.markdown(f"**CTA:** {plan.get('cta','')}")

                with st.expander("📝 SSML Segments"):
                    for seg in plan["segments"]:
                        st.code(seg["ssml"], language="xml")

                # Audio results
                with st.expander("🎵 Audio Production Results"):
                    st.json(data["audio"])

                # Download button
                final_file = data["audio"]["final_podcast"]
                try:
                    with open(final_file, "rb") as f:
                        st.download_button(
                            "⬇️ Download podcast.mp3",
                            f,
                            file_name="podcast.mp3",
                            mime="audio/mpeg",
                            key="download_text"
                        )
                except FileNotFoundError:
                    st.error(f"Could not find the generated file: {final_file}")
            else:
                st.error(f"❌ Pipeline failed: {result.get('error', 'Unknown error')}")

# Footer
st.markdown("---")
st.markdown("""
### 🤖 Agent Architecture Benefits
- **Modularity**: Each agent has a single responsibility
- **Maintainability**: Easy to update individual agents
- **Debugging**: Clear execution logs show which agent failed
- **Extensibility**: Easy to add new agents to the pipeline
- **Testability**: Each agent can be tested independently
""")