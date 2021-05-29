import sys, os
import re
from urllib.parse import urlparse
# sys.path.append(".")
import streamlit as st
import streamlit.components.v1 as components
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import graph
import links_crawler.main_crawler
from links_crawler.config import BAD_DOMAINS #domains to exclude from graph


def main():
    st.set_page_config(
        page_title="GraphMe",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("GraphMe")
    st.markdown("## Visualize all connections between site references")
    st.sidebar.title('Select graph options')
    link_input = st.sidebar.text_input("Enter link of the site to vizualize:", "https://support.unity3d.com/hc/en-us", key='input1')
    depth_input =  st.sidebar.text_input("Enter depth of crawling:", "2", key='input2')
    thread_input =  st.sidebar.text_input("Enter number of threads to crawling:", "20", key='input3')
    option=st.sidebar.selectbox('Select type',('Full links','Domains only'), key='box')
    # style=st.sidebar.checkbox('Add style interactivity') #feature does not work right now

    if(st.sidebar.button('Graph it!', key='button1')): #button to start crwaling and visualizing
        if re.match('^http.*', link_input.title().lower()): # .title() is used to get the input text string 
            initial_link = link_input.title().lower()
        else:
            initial_link = 'http://'+link_input.title().lower()

        all_links, all_domains = links_crawler.main_crawler.main_crawler(initial_link, int(thread_input.title()), int(depth_input.title())) #returns 2 dicts
        done = graph.make_graph(initial_link, all_links, all_domains, option)

        if done: #if make_graph() was sucessfully done
            HtmlFile = open("graphs/graphme.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read() 
            components.html(source_code, height = 800,width=1300)

    st.sidebar.title('Select saved graph')

    files = []
    path = os.path.abspath(os.getcwd())
    listdir = os.listdir('graphs/')
    for file in listdir:
        if re.match("^.*html$", file):
            files.append(file)

    saved_graphs = st.sidebar.selectbox('Show saved graphs',files)
    if(st.sidebar.button('Show it!', key='button2')): #button to show selected saved graph
        HtmlFile = open('graphs/'+saved_graphs.title().lower(), 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 800,width=1300)

    make_default_graph()

def make_default_graph(): 
    HtmlFile = open('graphs/google.com.html', 'r', encoding='utf-8') 
    source_code = HtmlFile.read() 
    components.html(source_code, height = 800,width=1300)

def create_database():
    engine = create_engine(f'postgresql://{username}:{password}@localhost/') #connect to psql without specific DB
    #create DB graphme if not exists:
    result = engine.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'graphme'") 
    exists = result.fetchone() 
    if not exists:
        session = sessionmaker(bind=engine)() #change isolation level is necessarily to create new DB
        session.connection().connection.set_isolation_level(0)
        session.execute('CREATE DATABASE graphme')
        session.connection().connection.set_isolation_level(1)
    engine.dispose()
    engine = create_engine(f'postgresql://{username}:{password}@localhost/graphme') #connect to created/existing graphme DB

    engine.execute("CREATE TABLE IF NOT EXISTS bad_domains (url text)") # create table of bad domains (domains to exclude from graph)
    engine.execute("TRUNCATE TABLE bad_domains") # clear table from old bad domains
    engine.execute("ALTER TABLE bad_domains ADD UNIQUE (url)") #make url column unique values only
    for domain in BAD_DOMAINS:
        engine.execute("INSERT INTO bad_domains (url) VALUES ('%s') ON CONFLICT (url) DO NOTHING"%domain) #add bad domains to this table


if __name__ == '__main__':
    username = "" #specify your postgres database username and pass
    password = ""
    # create_database() #uncomment this when username and pass are specified
    main()
