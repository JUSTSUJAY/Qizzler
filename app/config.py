import os
from dotenv import load_dotenv
import streamlit as st

def load_config():
    return load_dotenv()

def get_groq_api_key():
    return st.secrets["api_key"]
