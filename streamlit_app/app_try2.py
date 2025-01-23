import streamlit as st
import pandas as pd
from io import StringIO
import google.generativeai as genai
genai.configure(api_key="AIzaSyAWMp6F7RwJw2JEZEE3gQxfGsi-TCkvSs8")

# Function to generate test data
def generate_test_data(schema_df, num_records, column_name, instructions, separator="|"):
    try:
        mapping_text = schema_df
        column_name = schema_df[column_name].dropna().tolist()
        
        # Prompt for test data generation
        prompt = f""" Your role is synthetic data generator.
        List = {column_name} specifies the column names required in test data .
        Generate synthetic data for {num_records} rows in pipe separated values relevant to the column name given in List .
         Output Format:
        The response should include ONLY the generated synthetic data in as pipe separated values.
        Add header in the output.
        Do not include additional explanations, or comments in the output.
           """
        prompt = prompt + instructions
        st.write(prompt)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        test_data = pd.read_csv(StringIO(response.text), sep="|")
        st.subheader("Generated Data (Top 20 Records)")
        st.dataframe(test_data.head(20))
        return test_data.to_csv(index=False, sep='|')
    except Exception as e:
        return f"Error generating test data: {e}"

# Streamlit app
st.title("Synthetic Data Generator Dashboard")
st.write("Upload a schema file (CSV/Excel), specify the number of records, and generate synthetic data.")

# File upload
uploaded_file = st.file_uploader("Upload Schema File (CSV or Excel)", type=["csv", "xlsx"])
column_name = st.text_input("column containing schema")
instructions = st.text_input("custom instructions")

if uploaded_file:
    # Read uploaded file
    file_extension = uploaded_file.name.split('.')[-1]
    if file_extension == 'csv':
        schema_df = pd.read_csv(uploaded_file)
    elif file_extension == 'xlsx':
        schema_df = pd.read_excel(uploaded_file)
    
      # Display schema preview
    st.subheader("Uploaded Schema")
    st.dataframe(schema_df)
    # Input: Number of records
    num_records = st.number_input("Number of records to generate", min_value=1, max_value=100000, value=100)

    # Generate button
    if st.button("Generate Data"):
        with st.spinner("Generating synthetic data..."):
            generated_data = generate_test_data(schema_df, num_records, column_name,instructions)

            if generated_data:
                # Display top 20 records
                # Download button
                #csv_data = generated_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                        label="Download Data as CSV",
                        data=generated_data,
                        file_name="synthetic_data.csv",
                        mime="text/csv"
                    )
            else:
                st.error("Schema file must contain 'column_name' and 'data_type' columns.")

# Shareable link note
st.write("Deploy this app on a cloud platform (e.g., Streamlit Community Cloud, Heroku) to make it publicly accessible.")
