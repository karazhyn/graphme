import sys, os
import re
from urllib.parse import urlparse
# sys.path.append(".")
import streamlit as st
import streamlit.components.v1 as components
import graph
import links_crawler.main_crawler
# import logging
# from LinksCrawler.config import *
# from LinksCrawler.crawler import Crawler
try:
    st.set_page_config(
        page_title="GraphMe",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except: 
    pass

# Title
st.title("GraphMe")
st.markdown("## Visualize all connections between site references")


st.sidebar.title('Select graph options')
link_input = st.sidebar.text_input("Enter link of the site to vizualize:", "https://support.unity3d.com/hc/en-us")
depth_input =  st.sidebar.text_input("Enter depth of crawling:", "2")
thread_input =  st.sidebar.text_input("Enter number of threads to crawling:", "20")

option=st.sidebar.selectbox('Select type',('Full links','Domains only'))

# style=st.sidebar.checkbox('Add style interactivity') #feature does not work rn




# display the name when the submit button is clicked
# .title() is used to get the input text string 
if(st.sidebar.button('Graph it!')):
    # link = link_input.title()
    # st.success(result)
    if re.match('^http.*', link_input.title().lower()):
        initial_link = link_input.title().lower()
    else:
        initial_link = 'http://'+link_input.title().lower()

    all_links, external_links = links_crawler.main_crawler.main_crawler(initial_link, int(thread_input.title()), int(depth_input.title())) #returns 2 dicts
    
    print(external_links)
    done = graph.make_graph(initial_link, all_links, external_links, option)
    
    if done:
        HtmlFile = open("graphs/graphme.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 800,width=1300)

st.sidebar.title('Select saved graph')

files = os.listdir('graphs/')
files = [x for x in files if re.search("^.*html$", x)]
saved_graphs = st.sidebar.selectbox('Show saved graphs',files)

if(st.sidebar.button('Show it!')):

    HtmlFile = open('graphs/'+saved_graphs.title().lower(), 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 800,width=1300)