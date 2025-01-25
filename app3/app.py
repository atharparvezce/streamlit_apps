import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import docx
import PyPDF2
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS  # Standard stop words
import io
import pandas as pd

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with open(uploaded_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to handle text from uploaded file
def extract_text(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        return extract_text_from_docx(uploaded_file)
    elif file_extension == 'txt':
        return uploaded_file.read().decode("utf-8")
    else:
        st.error("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
        return None

# Streamlit UI
st.title("Word Cloud Generator")
st.write("Upload a text, PDF, or DOCX file to generate a word cloud and view word frequencies.")

# Upload file section
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

# Sidebar options
st.sidebar.title("Settings")

# Checkbox for standard stop words
use_standard_stopwords = st.sidebar.checkbox("Use Standard English Stop Words", value=False)

# Multi-select for random stop words (more diverse set of random stop words)
additional_stopwords = st.sidebar.multiselect(
    "Select Additional Stop Words (Optional)",
    options=[
        "the", "and", "is", "in", "this", "that", "it", "you", "to", "with", 
        "for", "as", "on", "by", "an", "at", "from", "of", "be", "have", "has",
        "were", "will", "are", "but", "they", "we", "he", "she", "him", "her",
        "me", "my", "myself", "ourselves", "yours", "yourself", "yourselves"
    ],
    default=[]
)

# Combine standard stop words with any selected ones
stop_words = set()

if use_standard_stopwords:
    stop_words.update(ENGLISH_STOP_WORDS)

stop_words.update(additional_stopwords)

# Width and Height sliders for word cloud dimensions
width_range = st.sidebar.slider("Word Cloud Width", min_value=400, max_value=1200, value=800)
height_range = st.sidebar.slider("Word Cloud Height", min_value=400, max_value=1200, value=400)

if uploaded_file is not None:
    # Extract text from the uploaded file
    text = extract_text(uploaded_file)
    
    if text:
        # Generate word cloud
        wordcloud = WordCloud(
            width=width_range, 
            height=height_range, 
            background_color="white", 
            stopwords=stop_words
        ).generate(text)
        
        # Display word cloud
        st.image(wordcloud.to_array(), caption="Word Cloud", use_column_width=True)
        
        # Save the word cloud as PNG below the image
        img_buffer = io.BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        st.download_button(
            label="Download Word Cloud as PNG",
            data=img_buffer,
            file_name="word_cloud.png",
            mime="image/png"
        )
        
        # Count word frequencies excluding stop words
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        word_counts = Counter(filtered_words)

        # Count stop words
        stop_word_counts = Counter([word for word in words if word.lower() in stop_words])

        # Combine word counts and stop word counts
        word_counts.update(stop_word_counts)

        # Create a sorted word count table (in decreasing order of counts)
        word_count_df = pd.DataFrame(word_counts.items(), columns=["Word", "Count"])
        word_count_df = word_count_df.sort_values(by="Count", ascending=False)

        # Display word count table
        st.write("Word Count Table (Excluding Stop Words):")
        st.dataframe(word_count_df)
        
        # Allow the user to download the word count table as CSV
        csv = word_count_df.to_csv(index=False)
        st.download_button(
            label="Download Word Count Table as CSV",
            data=csv,
            file_name="word_count_table.csv",
            mime="text/csv"
        )
