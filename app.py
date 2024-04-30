import streamlit as st
import requests
import json

# Streamlit UI layout
st.title('API Interaction Client')

# User can set the backend URL
BASE_URL = st.text_input("Enter Backend URL", value="http://127.0.0.1:8000")

def init_project(base_url, project_id, ai_search_conn, file_upload_conn, company_name, company_url, additional_info, callback_url):
    """Send initialization request to the API."""
    url = f"{base_url}/v0/projects/{project_id}/init"
    data = {
        "ai_search_conn": ai_search_conn,
        "file_upload_conn": file_upload_conn,
        "company_name": company_name,
        "company_url": company_url,
        "additional_information": additional_info,
        "callback_url": callback_url
    }
    response = requests.post(url, json=data)
    return response.json()

def query_project(base_url, project_id, company_background, query, query_params, response_format, callback_url):
    """Send a query request to the API."""
    url = f"{base_url}/v0/projects/{project_id}/query"
    data = {
        "company_background": company_background,
        "query": query,
        "query_params": query_params,
        "response_format": response_format,
        "callback_url": callback_url
    }
    response = requests.post(url, json=data)
    return response.json()

# Select the operation
operation = st.selectbox("Select the API Operation", ["Init Project", "Query Project"])

project_id = st.number_input("Enter Project ID", min_value=0, format='%d', value=0)

if operation == "Init Project":
    ai_search_conn = st.text_input("AI Search Connection String")
    file_upload_conn = st.text_input("File Upload Connection String")
    company_name = st.text_input("Company Name")
    company_url = st.text_input("Company URL")
    additional_info = st.text_area("Additional Information")
    callback_url = st.text_input("Callback URL", value='0.0.0.0')

    if st.button("Init Project"):
        result = init_project(BASE_URL, project_id, ai_search_conn, file_upload_conn, company_name, company_url, additional_info, callback_url)
        st.json(result)

elif operation == "Query Project":
    company_background = st.text_area("Company Background (JSON Format)")
    query = st.text_area("Query")
    # query_params = st.text_area("Query Parameters (JSON Format)")
    response_format = st.text_area("Response Format")
    # callback_url = st.text_input("Callback URL", value='0.0.0.0')

    if st.button("Query Project"):
        try:
            company_background = json.loads(company_background) if company_background else None
            query_params = {}
        except json.JSONDecodeError as e:
            st.error(f"JSON parsing error: {e}")
            st.stop()
        
        result = query_project(BASE_URL, project_id, company_background, query, query_params, response_format, "0.0.0.0")
        
        st.title("Response:")
        
        st.write(result['response'])
        