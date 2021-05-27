import sys, os
import re
from urllib.parse import urlparse
# sys.path.append(".")
import streamlit as st
import streamlit.components.v1 as components
import graph
import links_crawler.main_crawler
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import logging
# from LinksCrawler.config import *
# from LinksCrawler.crawler import Crawler


#try\except block made for handling st.set_page_config() bug
def main():
    st.set_page_config(
        page_title="GraphMe",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded"
    )


    # Title
    st.title("GraphMe")
    st.markdown("## Visualize all connections between site references")
    # Sidebar
    st.sidebar.title('Select graph options')
    link_input = st.sidebar.text_input("Enter link of the site to vizualize:", "https://support.unity3d.com/hc/en-us", key='input1')
    depth_input =  st.sidebar.text_input("Enter depth of crawling:", "2", key='input2')
    thread_input =  st.sidebar.text_input("Enter number of threads to crawling:", "20", key='input3')
    option=st.sidebar.selectbox('Select type',('Full links','Domains only'), key='box')
    # style=st.sidebar.checkbox('Add style interactivity') #feature does not work right now


    # display the name when the submit button is clicked
    # .title() is used to get the input text string 
    if(st.sidebar.button('Graph it!', key='button1')):
        if re.match('^http.*', link_input.title().lower()):
            initial_link = link_input.title().lower()
        else:
            initial_link = 'http://'+link_input.title().lower()

        all_links, external_links = links_crawler.main_crawler.main_crawler(initial_link, int(thread_input.title()), int(depth_input.title())) #returns 2 dicts
        
        print(external_links)
        done = graph.make_graph(initial_link, all_links, external_links, option)
        
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
            engine.execute("CREATE TABLE IF NOT EXISTS text_data (text varchar)")
            engine.execute("COPY text_data FROM '%s/graphs/lol.txt'"%(path))
            # engine.execute("INSERT INTO graphs (text) SELECT string_agg(text, chr(10)) FROM text_data")
            # engine.execute("DROP TABLE text_data")

        # engine.

    # files = [x for x in files if re.search("^.*html$", x)]
    saved_graphs = st.sidebar.selectbox('Show saved graphs',files)

    if(st.sidebar.button('Show it!', key='button2')):
        HtmlFile = open('graphs/'+saved_graphs.title().lower(), 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 800,width=1300)

if __name__ == '__main__':
    # connection = psycopg2.connect(user="postgres",
    #                             password='nimikita',
    #                             host="127.0.0.1",
    #                             port="5432",
    #                             database="graphme")

    # # Create a cursor to perform database operations
    # cursor = connection.cursor()
    # # Print PostgreSQL details
    # print("PostgreSQL server information")
    # print(connection.get_dsn_parameters(), "\n")
    # # Executing a SQL query
    # cursor.execute("SELECT version();")



    engine = create_engine('postgresql://postgres:nimikita@localhost/') #connect to psql without specific DB
    #create DB graphme if not exists:
    result = engine.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'graphme'") 
    exists = result.fetchone()
    if not exists:
        session = sessionmaker(bind=engine)() #change isolation level is necessarily to create new DB
        session.connection().connection.set_isolation_level(0)
        session.execute('CREATE DATABASE graphme')
        session.connection().connection.set_isolation_level(1)
    engine.dispose()
    engine = create_engine('postgresql://postgres:nimikita@localhost/graphme') #connect to created/existing graphme DB

    # engine.execute("SELECT 'CREATE DATABASE graphme' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'graphme')\gexec")
    engine.execute("CREATE TABLE IF NOT EXISTS graphs (graph text)")

    main()
