import streamlit as st
import spacy
import pandas as pd

# streamlit run app.py
# Language model map
LANG_MODELS = {
    "English": "en_core_web_sm",
    "German": "de_core_news_sm",
    "Spanish": "es_core_news_sm",
    "French": "fr_core_news_sm"
}

# Example sentences
EXAMPLES = {
    "English": "Apple is looking at buying a startup.",
    "German": "Apple erwägt den Kauf eines Startups.",
    "Spanish": "Apple está considerando comprar una startup.",
    "French": "Apple envisage d'acheter une startup."
}

# Streamlit page setup
st.set_page_config(page_title="POS Tagger - Multilingual", layout="centered")
st.title("🌐 Multilingual POS Tagger")
st.write("Enter a sentence and select a language to get Part-of-Speech tags.")

# Sidebar language selection
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox("Choose a language:", list(LANG_MODELS.keys()))

# Load selected language model
@st.cache_resource
def load_model(lang_code):
    return spacy.load(lang_code)

nlp = load_model(LANG_MODELS[language])

# Show example sentence
st.info(f"💡 Example: {EXAMPLES[language]}")

# Input text
text = st.text_area("Enter your sentence:", height=150)

# POS tagging logic
if st.button("Tag POS"):
    if not text.strip():
        st.warning("Please enter a sentence to tag.")
    else:
        doc = nlp(text)
        tagged_output = [{
            "Token": token.text,
            "POS": token.pos_,
            "POS Explanation": spacy.explain(token.pos_),
            "Tag": token.tag_,
            "Tag Explanation": spacy.explain(token.tag_) or "N/A"
        } for token in doc]

        df = pd.DataFrame(tagged_output)
        st.subheader("🔍 Tagged Tokens:")
        st.table(df)

        # CSV download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download as CSV", data=csv, file_name="pos_tags.csv", mime="text/csv")

# Clear input
if st.button("Clear"):
    st.experimental_rerun()
