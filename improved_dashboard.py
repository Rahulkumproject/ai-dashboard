import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Analyst",page_icon="🤖")
st.title(" 200k views AI dashbard")
api_key= st.sidebar.text_input("Enter google api key",type="password")
uploaded_file= st.file_uploader("Upload your Excel file",type=["xlsx"])
if uploaded_file:
    df=pd.read_excel(uploaded_file,engine="openpyxl")
    unique_account=df['Account_Name'].unique()
    option=st.sidebar.selectbox("select the account type",unique_account)
    filtered_df=df[df['Account_Name']==option]
    st.subheader(f"Data Preview for {option}")
    st.dataframe(filtered_df)
    st.divider()
    st.subheader("Customize your email")
    extra_instruction=st.text_area("Any extra instruction for AI",placeholder="offer 10% discount,firm message")

if api_key:
    genai.configure(api_key=api_key)
    model=genai.GenerativeModel('gemini-2.5-flash')
    company_name=filtered_df['Name']
    agreement_id=filtered_df['agreementId']
    if st.button("Draft Client Email."):
        with st.spinner("AI is composing an email"):
            prompt=f"""
            write a professional email to the client about this data:
            {df[df['Account_Name']==option].to_string()}
            important user instructions:
            {extra_instruction}
             """
            response=model.generate_content(prompt)
            st.success("AI Email Generated")
            st.markdown(response.text)
            st.download_button(
                label="Download Text File",
                data=response.text,
                file_name='simple_text.txt',
                mime='text/plain'
            )
