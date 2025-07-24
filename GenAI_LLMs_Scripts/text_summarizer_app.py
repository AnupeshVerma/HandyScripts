'''
    Run the command: streamlit run app.py
'''

import json
import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration


# ------------------ Backend: Summarization Function ------------------
def summarize_text(user_prompt):
    query_prompt = f"Summarize this text: \n" + user_prompt

      # Load the BART tokenizer and model
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

    # Tokenize input text and truncate if it exceeds model's max length
    inputs = tokenizer(query_prompt, return_tensors="pt", max_length=1024, truncation=True)  # This generates input_ids
    # Generate summary using beam search (num_beams=4)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=130, early_stopping=True)
    # Decode the generated summary IDs back into text
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return {
        "statusCode": 200,
        "body": json.dumps(summary)
    }   



# ------------------ Frontend: Streamlit UI ------------------
st.set_page_config(page_title='Text Summarizer')

new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">Text Summarizer 🎯</p>'
st.markdown(new_title, unsafe_allow_html=True)

input_text = st.text_area("Enter text to summarize:")

if st.button("Summarize"):
    if input_text.strip():
        response = summarize_text(input_text)
        st.subheader("Summary")
        st.write(response['body'])
    else:
        st.warning("Please enter some text to summarize.")