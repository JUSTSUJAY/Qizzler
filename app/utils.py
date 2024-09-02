from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import load_config, get_groq_api_key
from PyPDF2 import PdfReader

load_config()

def get_llm():
    llm  = ChatGroq(api_key=get_groq_api_key(), model='llama-3.1-70b-versatile', temperature=0.7)
    return llm

def get_prompt_template_for_questions(question_type):
    prompt_template = ChatPromptTemplate.from_template(
        f"""You're a teaching assistant. Create a list of {question_type} questions along with their answers from the given content:
        Strict Guidelines:
            1. If the user has asked for True False Questions, create questions that can be answered with a simple True or False.
            2. If the user has asked for MCQ Questions, create questions that have 4 options and only one of them is correct.
            3. If the user has asked for One Word answer questions, create questions that can be answered with a single word or a single phrase, make sure it is not a long sentence answer at any cost.
            4. If the user has asked for MCQ Questions, make sure the answer is one of the options.
            5. Craft Questions from the content provided so that everything is covered and the entire understanding of the user can be tested without repeating the question.
            6. Do not include any explanations or explanations in the questions.
        These Strict Guidelines must be adhered to at all costs.
        Content: {{content}}
        Provide the questions and answers only, nothing more.
        """
    )
    
    # LLMChain class has been deprecated in Langchain and the solution was to create a runnablesequence instead. 
    # https://api.python.langchain.com/en/latest/chains/langchain.chains.llm.LLMChain.html
    question_chain = prompt_template | get_llm() | StrOutputParser()
    return question_chain

def save_questions_to_file(filename, questions):
    with open(filename, 'w') as file:
        for question in questions:
            file.write(question + "\n")

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text