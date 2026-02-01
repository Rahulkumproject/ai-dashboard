import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="AI Analyst", page_icon="🤖", layout="wide")
st.title("🤖 Rahul's AI Smart Analyst")

# --- SIDEBAR ---
api_key = st.sidebar.text_input("Enter google api key", type="password")
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx"])

# --- TABS ---
tab1, tab2 = st.tabs(["📧 Email Generator", "📈 Analytics Dashboard"])

if api_key and uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")

    # --- TAB 1: EMAIL GENERATOR ---
    with tab1:
        st.header("Draft Client Emails")

        # 1. The Dropdown
        option = st.selectbox("Select Client Account", df['Account_Name'].unique())

        # 2. Custom Instructions
        st.divider()
        extra_instructions = st.text_area(
            "Custom Instructions for AI:",
            placeholder="e.g., Offer a 10% discount, Be very firm..."
        )

        # 3. The Button
        if st.button("Draft Client Email"):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')

            with st.spinner("Writing email..."):
                # Filter data
                client_data = df[df['Account_Name'] == option].to_string()

                # Prompt
                prompt = f"""
                Write a professional email for this client data:
                {client_data}

                IMPORTANT USER INSTRUCTIONS:
                {extra_instructions}

                Sign it as 'The Accounts Team'.
                """

                response = model.generate_content(prompt)

                # Output
                st.success("Draft Generated!")
                st.markdown(response.text)

                # Download
                st.download_button(
                    label="📥 Download Email Draft",
                    data=response.text,
                    file_name=f"email_for_{option}.txt",
                    mime="text/plain"
                )

    # --- TAB 2: ANALYTICS DASHBOARD ---
    with tab2:
        st.header("Data Insights")

        # Metric Cards
        col1, col2 = st.columns(2)
        col1.metric("Total Agreements", len(df))
        col2.metric("Unique Clients", df['Account_Name'].nunique())

        # The Chart
        st.subheader("Agreements per Client")
        st.bar_chart(df['Account_Name'].value_counts())

        # Raw Data View
        with st.expander("View Raw Data"):
            st.dataframe(df)

else:
    st.info("Please upload a file and enter your API key to begin.")