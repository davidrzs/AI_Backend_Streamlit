import streamlit as st
import requests
import json

# Streamlit UI layout
st.title('API Interaction Client')

# User can set the backend URL
BASE_URL = st.text_input("Enter Backend URL", value="http://127.0.0.1:8000")

def query_project(base_url, project_id, company_background, query, response_format, callback_url, tools, ai_search_endpoint, ai_search_api_key, ai_search_index_name):
    """Send a query request to the API."""
    url = f"{base_url}/v0/projects/{project_id}/query_agent"
    data = {
        "company_background": company_background,
        "query": query,
        "response_format": response_format,
        "callback_url": callback_url,
        "tools": tools,
        "tenant_id": 0,  # Hardcoded for now, will be removed in the future
        "ai_search_endpoint": ai_search_endpoint,
        "ai_search_api_key": ai_search_api_key,
        "ai_search_index_name": ai_search_index_name
    }
    response = requests.post(url, json=data)
    return response.json()


# Project ID
project_id = 12#st.number_input("Enter Project ID", min_value=0, format='%d', value=0)

# Query Project
company_background = st.text_area("Company Background (JSON Format)")    
query = st.text_area("Query")
response_format = st.text_area("Response Format")
callback_url = ""#st.text_input("Callback URL", value='http://127.0.0.1:8000/callback')
ai_search_endpoint = ""#st.text_input("AI Search Endpoint")
ai_search_api_key = ""# st.text_input("AI Search API Key")
ai_search_index_name = ""#st.text_input("AI Search Index Name")

# Tools selection
available_tools = ["bundesanzeiger", "news", "search", "calculate", "scraper"]
selected_tools = []
for tool in available_tools:
    if st.checkbox(f"{tool} tool", key=tool):
        selected_tools.append(tool)

if st.button("Query Project"):
    try:
        company_background = json.loads(company_background) if company_background else None
    except json.JSONDecodeError as e:
        st.error(f"JSON parsing error: {e}")
        st.stop()
    
    result = query_project(BASE_URL, project_id, company_background, query, response_format, callback_url, selected_tools, ai_search_endpoint, ai_search_api_key, ai_search_index_name)
    
    st.title("Response:")
    print(result)
    
    st.write(result['response'])
