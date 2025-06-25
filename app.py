import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Function to get Gemini response
def get_gemini_repsonse(prompt):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Streamlit UI Setup
st.set_page_config(page_title="Smart ATS", page_icon="📄", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📄 Smart ATS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🚀 Enhance your resume by matching it with your dream job description</p>", unsafe_allow_html=True)
st.markdown("---")

# Inputs
st.markdown("### 📋 Paste the Job Description")
jd = st.text_area("Enter JD here...", height=200)

st.markdown("### 📎 Upload Your Resume (PDF only)")
uploaded_file = st.file_uploader("Upload your resume", type="pdf")

submit = st.button("🔍 Analyze Resume")

if submit:
    if uploaded_file is not None and jd.strip() != "":
        resume_text = input_pdf_text(uploaded_file)

        formatted_prompt = f"""
        Act as a highly skilled ATS (Applicant Tracking System) used by top tech recruiters.

        You have deep understanding of evaluating resumes in fields like software development, data science,
        and engineering. Evaluate the resume below against the given job description.

        Provide your output in readable plain text format — do NOT use JSON.
        Start with:
        1. JD Match Percentage
        2. Missing Keywords (as a bullet list)
        3. A brief and impactful Profile Summary
        4. Detailed Evaluation (education, projects, skills, suggestions)

        -------------------------------
        Resume:
        {resume_text}

        -------------------------------
        Job Description:
        {jd}
        """

        with st.spinner("🔍 Analyzing your resume..."):
            try:
                response = get_gemini_repsonse(formatted_prompt)

                # Headers
                st.markdown("---")
                st.markdown("## 📊 <span style='color:#FF5733'>ATS Evaluation Result</span>", unsafe_allow_html=True)

                # Parse sections
                lines = response.splitlines()
                match_line = next((line for line in lines if "JD Match" in line), "JD Match: 0%")
                match_percent_str = match_line.split(":")[1].strip().replace("%", "")
                match_percent = int(match_percent_str) if match_percent_str.isdigit() else 0

                st.markdown(f"### ✅ JD Match: **{match_percent}%**")
                st.progress(match_percent / 100.0)

                # Section processing
                missing_kw_text = ""
                profile_summary_text = ""
                detailed_evaluation_text = ""
                current_section = None

                for line in lines:
                    line_lower = line.lower().strip()
                    if "missing keyword" in line_lower:
                        current_section = "missing"
                        continue
                    elif "profile summary" in line_lower:
                        current_section = "summary"
                        continue
                    elif "detailed evaluation" in line_lower:
                        current_section = "evaluation"
                        continue

                    if current_section == "missing":
                        missing_kw_text += line + "\n"
                    elif current_section == "summary":
                        profile_summary_text += line + "\n"
                    elif current_section == "evaluation":
                        detailed_evaluation_text += line + "\n"

                # 🔍 Missing Keywords
                st.markdown("### 🔍 <span style='color:#e53935'>Missing Keywords</span>", unsafe_allow_html=True)
                if missing_kw_text.strip():
                    bullets = [kw.strip("•-* ") for kw in missing_kw_text.strip().splitlines() if kw.strip()]
                    for kw in bullets:
                        st.markdown(f"• {kw}")
                else:
                    st.success("No important keywords missing. Great job! 🎉")

                # 🧠 Profile Summary
                st.markdown("### 🧠 <span style='color:#0288D1'>Profile Summary</span>", unsafe_allow_html=True)
                if profile_summary_text.strip():
                    st.markdown(
                        f"<div style='color:#0288D1;font-size:16px;font-weight:500;padding:10px 0;'>{profile_summary_text.strip()}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.info("No profile summary provided.")

                # 📌 Detailed Evaluation
                st.markdown("### 📌 <span style='color:#8E24AA'>Detailed Evaluation</span>", unsafe_allow_html=True)
                if detailed_evaluation_text.strip():
                    if "**Suggestions:**" in detailed_evaluation_text:
                        main_eval, suggestions = detailed_evaluation_text.split("**Suggestions:**", 1)
                    else:
                        main_eval, suggestions = detailed_evaluation_text, ""

                    # Main Evaluation
                    st.markdown(
                        f"""
                        <div style='color:#FAFAFA; font-size:15px; line-height:1.8; background-color:#2c2f33; padding:15px; border-radius:10px;'>
                        {main_eval.strip().replace("**", "<b>").replace("*", "")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Suggestions as bullets
                    if suggestions.strip():
                        st.markdown("#### 💡 Suggestions")
                        for line in suggestions.strip().splitlines():
                            if line.strip().startswith("*"):
                                st.markdown(f"• {line.strip().lstrip('* ').replace('**', '**')}")
                else:
                    st.info("No detailed evaluation provided.")

                # 📥 Download button
                st.download_button(
                    label="📥 Download ATS Report",
                    data=response,
                    file_name="ATS_Report.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error("❌ Error analyzing the resume. Here's the raw response:")
                st.code(str(e))
    else:
        st.warning("⚠️ Please upload a resume and paste a job description.")
