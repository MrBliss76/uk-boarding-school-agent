import streamlit as st
from scraper import fetch_results_for_school, SCHOOLS

st.title("🏫 UK Boarding School Results Explorer")

school = st.selectbox("Select a school", list(SCHOOLS.keys()))

st.markdown(f"### 📊 Results for {school}")
with st.spinner("Fetching exam results..."):
    results = fetch_results_for_school(school)

if not results:
    st.warning("No results found.")
else:
    for src, exams in results.items():
        st.subheader(f"📄 Source: {src}")
        if isinstance(exams, dict):
            for exam, line in exams.items():
                st.markdown(f"**{exam}**: {line}")
        else:
            st.markdown(exams)
