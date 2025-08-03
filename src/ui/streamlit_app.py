import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
load_dotenv()
from email_header_analyzer.core.parser import EmailHeaderParser

def main():
    st.set_page_config(page_title="Email Header Analyzer", layout="wide")
    st.title("Email Header Analyzer")
    st.sidebar.header("Options")
    mode = st.sidebar.selectbox("Mode", ["Full", "Quick", "Auth Only"])
    geo = st.sidebar.checkbox("Geographic", True)
    content = st.sidebar.checkbox("Content", True)
    raw = st.text_area("Paste headers", height=200)
    if st.button("Analyze"):
        if not raw.strip():
            st.error("Provide headers")
        else:
            try:
                res = EmailHeaderParser().analyze_headers(raw)
                display(res, geo, content)
            except Exception as e:
                st.error(f"Failed: {e}")

def display(res, geo, content):
    st.subheader("Risk Scores")
    cols = st.columns(4)
    cols[0].metric("Auth", f"{res['authentication']['score']}/100")  
    cols[1].metric("Spoof", f"{res['spoofing']['risk_score']}/100")  
    cols[2].metric("Content", f"{res['content']['risk_score']}/100" if content else "Disabled")
    cols[3].metric("Issues", sum(len(s.get("issues", [])) for s in res.values() if isinstance(s, dict)))
    tabs = ["Summary", "Auth", "Routing", "Spoofing"]
    if geo:
        tabs.append("Geo")
    if content:
        tabs.append("Content")
    tabs.append("Raw")
    t = st.tabs(tabs)
    with t[0]:
        st.write(res['summary'])
    with t[1]:
        st.write(res['authentication'])
    with t[2]:
        st.write(res['routing'])
    with t[3]:
        st.write(res['spoofing'])
    idx = 4
    if geo:
        with t[idx]:
            st.write(res['geographic'])
        idx += 1
    if content:
        with t[idx]:
            st.write(res['content'])
        idx += 1
    with t[idx]:
        st.write(res['parsed_headers'])

if __name__ == "__main__":
    main()
