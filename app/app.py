# import necessary libs
import streamlit as st
from utils import extract_text_from_pdf, get_prompt_template_for_questions, save_questions_to_file

# Configure the Streamlit app
st.set_page_config(page_title='Qizzler', page_icon='❓')
st.title("Qizzler")

# Task 1: Load PDF
st.subheader("Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# when the file is uploaded, extract the text from the pdf and we can start working with the text content
if uploaded_file:
    content = extract_text_from_pdf(uploaded_file)

    # Task 2: Generate Questions, will give a dropdown for the question type
    st.subheader("Select Question Type")
    question_type = st.selectbox("Choose the type of questions to generate", ["True or False", "One Word answer questions", "MCQ"])

    generate_btn = st.button("Generate Questions")

    if generate_btn:
        with st.spinner(f"Generating {question_type} questions..."):
            question_chain = get_prompt_template_for_questions(question_type)
            questions_str = question_chain.invoke({'content': content})
            questions_and_answers = questions_str.split("\n")
            save_filename = f"{question_type}_questions.txt"
            save_questions_to_file(save_filename, questions_and_answers)
            st.success(f"Questions saved!")
            st.subheader("Generated Questions and Answers")
            for qa in questions_and_answers:
                st.write(qa)

            # download button to download the text file of questions and answers generated
            with open(save_filename, 'rb') as file:
                st.download_button(label="Download Questions", data=file, file_name=save_filename, mime='text/plain')

