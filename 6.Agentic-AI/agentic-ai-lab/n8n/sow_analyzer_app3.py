import streamlit as st
import requests
import json
import pandas as pd
import re
import concurrent.futures

st.set_page_config(page_title="SOW Analyzer", layout="centered")
st.title("SOW Analyzer")

# File uploader
uploaded_file = st.file_uploader("Upload your PDF or DOCX SOW file", type=["pdf", "docx"])

# Webhook URL input
webhook_url = st.text_input("Enter your n8n webhook URL", "")



def display_scope(scope):
    if scope:
        st.subheader("Scope")
        df_scope = pd.DataFrame([scope])
        st.table(df_scope)
    else:
        st.info("No scope data found.")

        
def display_terms(terms, scrollable=True):
    if terms:
        st.subheader("Terms & Conditions")

        # Convert {term: extracted} dict into DataFrame
        df_terms = pd.DataFrame(list(terms.items()), columns=["Term", "Extracted"])

        if scrollable:
            # Option 1: Scrollable + resizable table
            st.dataframe(df_terms, width='stretch')
        else:
            # Option 2: Static table with text wrapping
            styled_df = df_terms.style.set_properties(**{
                'white-space': 'pre-wrap',
                'word-wrap': 'break-word'
            })
            st.table(styled_df)
    else:
        st.info("No terms data found.")        

def display_roles(roles):
    if roles:
        st.subheader("Roles & Responsibilities")
        df_roles = pd.DataFrame(roles)
        st.table(df_roles)
    else:
        st.info("No roles data found.")
        
# Function to extract JSON from Markdown code block
def extract_json_from_content(content):
    match = re.search(r"```json\s*([\s\S]*?)```", content)
    if not match:
        print("results not found")
        return None
    try:
        print("I'm in match")
        return json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print("Invalid JSON:", e)
        return None

def extract_json_from_content2(content):
    #match = re.search(r"```json\s*([\s\S]*?)```", content)
    match=re.findall(r"```json\s*([\s\S]*?)```", content)
    
    json_objects=[]
    for json_str in match:
        try:
            obj = json.loads(json_str)
            #print(obj)
            
            json_objects.append(obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e} - String: {json_str}")
    return json_objects        
 
def extract_terms_and_extracted(data, as_dict_list=False):
    """
    Extracts 'term' and 'extracted' values from the given JSON structure.

    Args:
        data (list): List containing dictionaries with 'terms' key.
        as_dict_list (bool):
            - True  → return as list of dicts [{term, extracted}, ...]
            - False → return as flat dict {term: extracted}

    Returns:
        list | dict
    """
    if not data:
        return {} if not as_dict_list else []

    if as_dict_list:
        # Return as list of dicts
        return [
            {"term": t.get("term"), "extracted": t.get("extracted")}
            for item in data
            for t in item.get("terms", [])
        ]
    else:
        # Return as flat dictionary
        return {
            t.get("term"): t.get("extracted")
            for item in data
            for t in item.get("terms", [])
        }






def parse_results(data):
    
    all_scope = []
    all_terms = []
    content_jsons=[]
    #Sst.subheader(data[0]['message']['content'])
    for item in data:
        #message = item.get("message", {})
        #content = message.get("content", "")
        
        content_jsons.append(extract_json_from_content2(item['message']['content']))
  

    if(not all_scope):
           all_scope = content_jsons[0][0]["scope"]["summary"]
           
    if(not all_terms):   
          all_terms = extract_terms_and_extracted(content_jsons[1])
       
        
     
        
    final_results = {
        "scope": all_scope,
        "terms": all_terms
         }
    # Print to console
    #return json.dumps(final_results)
    return final_results

def make_request():
    
    files = {"data": (uploaded_file.name, uploaded_file, "application/octet-stream")}
    return requests.post(webhook_url, files=files, timeout=10000)
result_json=None

if uploaded_file and webhook_url:
    if st.button("Analyze SOW"):
        try:
            with st.spinner("Processing..."):
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future=executor.submit(make_request)
                    response=future.result(timeout=10000)
                    #print(response.json())
            #files = {"data": (uploaded_file.name, uploaded_file, "application/octet-stream")}
            #response = requests.post(webhook_url, files=files)
            #st.subheader(response.json())
            #response.raise_for_status()
            
                    result_json = parse_results(response.json())
                    #result_json = response.json()
                    if result_json:
                        st.success("Analysis Complete!")
                        
                        # Display each section separately
                        display_scope(result_json.get("scope"))
                        display_terms(result_json.get("terms"))
                        display_roles(result_json.get("roles"))

            # Add download button
            st.download_button(
                label="Download JSON Result",
                data=json.dumps(result_json, indent=2),
                file_name="sow_analysis_result.json",
                mime="application/json"
            )
            
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
        except json.JSONDecodeError:
            st.error("Response is not valid JSON")