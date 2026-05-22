import streamlit as st
import os
import io
from agent import run_research_stream

st.set_page_config(page_title="AI Research Agent", page_icon="🔍")
st.title("🔍 AI Research Agent")
st.write("Enter any topic and the agent will autonomously search the web and write a research report.")

# Session state
if "reports" not in st.session_state:
    st.session_state.reports = []

# Sidebar
with st.sidebar:
    st.header("Setup")
    openai_key = st.text_input("OpenAI API Key", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key

    if st.session_state.reports:
        st.divider()
        st.header("Search History")
        for i, r in enumerate(st.session_state.reports):
            st.caption(f"{i+1}. {r['topic']}")
        if st.button("Clear History"):
            st.session_state.reports = []
            st.rerun()

# Main input
topic = st.text_input("Research topic", placeholder="e.g. Latest developments in AI agents 2026")

if st.button("Research", type="primary"):
    if not openai_key or not tavily_key:
        st.warning("Please enter both API keys in the sidebar.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        st.divider()
        st.subheader("Agent Activity")
        activity_container = st.container()
        report_container = st.empty()
        final_report = ""

        with activity_container:
            for update_type, content in run_research_stream(topic):
                if update_type == "search":
                    st.markdown(content)
                elif update_type == "result":
                    st.markdown(content)
                elif update_type == "report":
                    final_report = content

        if final_report:
            st.divider()
            st.subheader("Research Report")
            st.markdown(final_report)

            # Save to history
            st.session_state.reports.append({
                "topic": topic,
                "report": final_report
            })

            # Download button
            st.download_button(
                label="Download Report as .txt",
                data=final_report,
                file_name=f"{topic[:30].replace(' ', '_')}_report.txt",
                mime="text/plain"
            )

# Show previous reports
if st.session_state.reports:
    st.divider()
    st.subheader("Previous Reports")
    for r in reversed(st.session_state.reports[:-1] if st.session_state.reports else []):
        with st.expander(f"📄 {r['topic']}"):
            st.markdown(r["report"])
            st.download_button(
                label="Download",
                data=r["report"],
                file_name=f"{r['topic'][:30].replace(' ', '_')}_report.txt",
                mime="text/plain",
                key=r["topic"]
            )
