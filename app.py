from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
from PyPDF2 import PdfReader
import google.generativeai as genai
import subprocess

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read PDF content using PyPDF2
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()

        if not pdf_text.strip():
            raise ValueError("No extractable text found in the PDF. Ensure the PDF contains text layers.")

        # Prepare PDF content for API
        pdf_parts = [
            {
                "mime_type": "text/plain",
                "data": base64.b64encode(pdf_text.encode('utf-8')).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("Percentage match")
submit4 = st.button("Tell Me Keywords Missing")
submit5 = st.button("Make My Resume Match the Job Description")
submit6 = st.button("Suggest Some Certifications and Courses to Improve My Resume")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager with experience in field of any one job role from  Frontend Developer, Backend Developer, Full Stack Developer, Mobile App Developer, Game Developer , Data Scientist, Data Analyst, Data Engineer, Business Intelligence Analyst , AI Engineer, Machine Learning Engineer, Deep Learning Engineer, NLP Engineer, Cybersecurity Analyst, Ethical Hacker, Security Engineer, Incident Responder, Cloud Engineer, DevOps Engineer, Site Reliability Engineer (SRE), Quality Assurance Engineer, Automation Tester , Network Administrator, System Administrator, Cloud Systems Administrator, Database Administrator, Big Data Engineer, Blockchain Developer, AR/VR Developer, IoT Developer, Research Scientist, University Lecturer/Professor, Product Manager, UI/UX Designer, Tech Support Engineer, Freelancer/Consultant,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""
input_prompt2 = """
You are an experienced Career Coach with expertise in evaluating resumes for roles such as Frontend Developer, Backend Developer, Full Stack Developer, Mobile App Developer, Game Developer, Data Scientist, Data Analyst, Data Engineer, Business Intelligence Analyst, AI Engineer, Machine Learning Engineer, Deep Learning Engineer, NLP Engineer, Cybersecurity Analyst, Ethical Hacker, Security Engineer, Incident Responder, Cloud Engineer, DevOps Engineer, Site Reliability Engineer (SRE), Quality Assurance Engineer, Automation Tester, Network Administrator, System Administrator, Cloud Systems Administrator, Database Administrator, Big Data Engineer, Blockchain Developer, AR/VR Developer, IoT Developer, Research Scientist, University Lecturer/Professor, Product Manager, UI/UX Designer, Tech Support Engineer, and Freelancer/Consultant. 

Your task is to analyze the provided resume and job description, then offer actionable suggestions to improve the applicant's skills, certifications, or achievements to better align with the role. Highlight specific areas of improvement and suggest relevant resources or certifications.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of  any one job role from  Frontend Developer, Backend Developer, Full Stack Developer, Mobile App Developer, Game Developer , Data Scientist, Data Analyst, Data Engineer, Business Intelligence Analyst , AI Engineer, Machine Learning Engineer, Deep Learning Engineer, NLP Engineer, Cybersecurity Analyst, Ethical Hacker, Security Engineer, Incident Responder, Cloud Engineer, DevOps Engineer, Site Reliability Engineer (SRE), Quality Assurance Engineer, Automation Tester , Network Administrator, System Administrator, Cloud Systems Administrator, Database Administrator, Big Data Engineer, Blockchain Developer, AR/VR Developer, IoT Developer, Research Scientist, University Lecturer/Professor, Product Manager, UI/UX Designer, Tech Support Engineer, Freelancer/Consultant and ATS functionality,your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches the job description. First the output should come as percentage .
"""
input_prompt4 = """
You are an ATS (Applicant Tracking System) expert and resume optimization specialist. Your task is to compare the uploaded resume with the provided job description for roles such as Frontend Developer, Backend Developer, Full Stack Developer, Mobile App Developer, Game Developer, Data Scientist, Data Analyst, Data Engineer, Business Intelligence Analyst, AI Engineer, Machine Learning Engineer, Deep Learning Engineer, NLP Engineer, Cybersecurity Analyst, Ethical Hacker, Security Engineer, Incident Responder, Cloud Engineer, DevOps Engineer, Site Reliability Engineer (SRE), Quality Assurance Engineer, Automation Tester, Network Administrator, System Administrator, Cloud Systems Administrator, Database Administrator, Big Data Engineer, Blockchain Developer, AR/VR Developer, IoT Developer, Research Scientist, University Lecturer/Professor, Product Manager, UI/UX Designer, Tech Support Engineer, and Freelancer/Consultant. 

Evaluate the resume and identify key skills, technologies, or keywords missing that are critical for the job description. List the missing keywords clearly, and explain their importance in the context of the role.
"""
input_prompt5 = """
You are a resume writing expert and ATS optimization specialist for roles such as Frontend Developer, Backend Developer, Full Stack Developer, Mobile App Developer, Game Developer, Data Scientist, Data Analyst, Data Engineer, Business Intelligence Analyst, AI Engineer, Machine Learning Engineer, Deep Learning Engineer, NLP Engineer, Cybersecurity Analyst, Ethical Hacker, Security Engineer, Incident Responder, Cloud Engineer, DevOps Engineer, Site Reliability Engineer (SRE), Quality Assurance Engineer, Automation Tester, Network Administrator, System Administrator, Cloud Systems Administrator, Database Administrator, Big Data Engineer, Blockchain Developer, AR/VR Developer, IoT Developer, Research Scientist, University Lecturer/Professor, Product Manager, UI/UX Designer, Tech Support Engineer, and Freelancer/Consultant.

Your task is to modify the provided resume to align it perfectly with the job description. Recommend specific changes to the skills, experience, or format of the resume to increase its ATS compatibility and make it more appealing to recruiters.
"""
input_prompt6 = """
You are a professional Career Advisor specializing in identifying key certifications and courses for roles such as Frontend Developer, Backend Developer, Full Stack Developer, Mobile App Developer, Game Developer, Data Scientist, Data Analyst, Data Engineer, Business Intelligence Analyst, AI Engineer, Machine Learning Engineer, Deep Learning Engineer, NLP Engineer, Cybersecurity Analyst, Ethical Hacker, Security Engineer, Incident Responder, Cloud Engineer, DevOps Engineer, Site Reliability Engineer (SRE), Quality Assurance Engineer, Automation Tester, Network Administrator, System Administrator, Cloud Systems Administrator, Database Administrator, Big Data Engineer, Blockchain Developer, AR/VR Developer, IoT Developer, Research Scientist, University Lecturer/Professor, Product Manager, UI/UX Designer, Tech Support Engineer, and Freelancer/Consultant.

Analyze the provided resume and job description to recommend relevant certifications, courses, or training programs that will strengthen the candidate's profile for the role. Ensure the suggestions are specific to the job description and industry requirements.
"""


if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt5, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit6:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt6, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
