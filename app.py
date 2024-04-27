import streamlit as st
import requests
import json

# Set the base URL for API requests
BASE_URL = "https://ai.backend.ddmind.ai"

def init_project(project_id, company_name, company_url, additional_info, callback_url):
    """Send initialization request to the API."""
    url = f"{BASE_URL}/v0/projects/{project_id}/init"
    data = {
        "company_name": company_name,
        "company_url": company_url,
        "additional_information": additional_info,
        "callback_url": callback_url
    }
    response = requests.post(url, json=data)
    return response.json()

def query_project(project_id, company_background, query, query_params, response_format, callback_url):
    """Send a query request to the API."""
    url = f"{BASE_URL}/v0/projects/{project_id}/query"
    data = {
        "company_background": company_background,
        "query": query,
        "query_params": query_params,
        "response_format": response_format,
        "callback_url": callback_url
    }
    response = requests.post(url, json=data)
    return response.json()

# Streamlit UI layout
st.title('API Interaction Client')

# Select the operation
operation = st.selectbox("Select the API Operation", ["Init Project", "Query Project"])

project_id = st.number_input("Enter Project ID", min_value=0, format='%d')

if operation == "Init Project":
    company_name = st.text_input("Company Name")
    company_url = st.text_input("Company URL")
    additional_info = st.text_area("Additional Information")
    callback_url = st.text_input("Callback URL", value='0.0.0.0')

    if st.button("Init Project"):
        result = init_project(project_id, company_name, company_url, additional_info, callback_url)
        st.json(result)

elif operation == "Query Project":
    company_background = st.text_area("Company Background (JSON Format)")
    query = st.text_input("Query")
    query_params = st.text_area("Query Parameters (JSON Format)")
    response_format = st.selectbox("Response Format", ["free_text", "json_list"])
    callback_url = st.text_input("Callback URL", value='0.0.0.0')

    if st.button("Query Project"):
        # Convert text input into JSON
        try:
            company_background = json.loads(company_background) if company_background else None
            query_params = json.loads(query_params) if query_params else None
        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {e}")
            st.stop()
        
        result = query_project(project_id, company_background, query, query_params, response_format, callback_url)
        st.json(result)
