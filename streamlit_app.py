# Step01 == Create a streamlit user interface
# Step02 == Grab data from the target website

from scrape import website_scraper, clean_body_content,extract_body_content,split_dom_content, website_scraper_with_proxies
import streamlit as st
from parse import parse_with_ollama

st.set_page_config(page_title="Web-scraper")
st.title("Web-scraping with AI") # title of the webpage

st.session_state.url = st.text_input("Enter the target URL: ") # To ask user to enter the website url he wants to scrape

if st.button("Scrape the target website url"):
    st.write("Scraping the website")
    result = website_scraper(website_url=st.session_state.url)      
    
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    
    st.session_state.dom_content = cleaned_content # to store in streamlit session
    
    with st.expander("View the scraped content"):
        st.text_area("Scraped content", cleaned_content, height=500)

    print("Done with scraping.") 
    

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want from the DOM content:")
    
    if st.button("Parse content"):
        if parse_description:
            st.write("Parsing the content")
            
            dom_chunks = split_dom_content(st.session_state.dom_content) 
            
            result = parse_with_ollama(dom_chunks, parse_description)
            
            st.write(result)
            st.success(body="Success in Parsing content")
            
            
            
               
