# GraphMe
### Crawl and visualize all connections between site references with certain depth of crawling.

## Appearance
![screenshot1](screenshots/demo1.png)
![screenshot2](screenshots/demo2.png)

## Features
* Crawl all links in site with certain depth of recursion
* Visualize these links with interactive network graph
* Option to visualize full link\domain only
* Option to choose depth of crawling and number of threads to crawling
* Save and load graph

## Install and run
'''
git clone https://github.com/karazhyn/graphme
cd graphme
pip install -r requirements.txt
python3 main.py
streamlit run main.py
'''
