import sys, os
import math
from urllib.parse import urlparse
from pyvis.network import Network
import main
from links_crawler.main_crawler import main_crawler


def make_graph(initial_link, all_links, all_domains, option):
    got_net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

    # set the physics layout of the network
    got_net.barnes_hut()

    if option == 'Full links':
        if all_links: #if not empty
            keys = []
            length = []
            for key in all_links.keys(): #make main red nodes 
                keys.append(key)
                length.append(len(all_links[key]))
            for src, size in zip(keys, length):
                got_net.add_node(src,src, size=13+math.log2(int(size)**6), title=src, color = 'red')


            for src, edges in all_links.items(): #make other nodes
                got_net.add_node(src, src, size=len(edges)*5, title=src, color='green')
                for dst in edges:
                    got_net.add_node(dst, dst, title=dst, color='white')
                    got_net.add_edge(src, dst)
                    print(f'New edge: {src}: {dst}')
            
            # make a font size smaller
            got_net.set_options(''' 
            var options = {
                "nodes": {
                    "borderWidthSelected": 3,
                    "font": {
                        "color": "rgba(117,117,117,1)",
                        "size": 10,
                        "face": "arial",
                        "strokeWidth": 1
                    },
                    "size": 13
                }
            }
            ''')

            initial_link = urlparse(initial_link).netloc #name graph as domain name
            if initial_link.split('.')[0] == 'www': 
                initial_link = initial_link[4:]
            
            got_net.save_graph('graphs/'+initial_link+'.html')
            got_net.save_graph('graphs/graphme.html') #graphme is always the last saved graph
            return True #return that everything is ok
                    
        else: #if list is empty
            main.st.warning('Site has anti-parsing system. Choose another one.')
            return False #something went wrong

    elif option == 'Domains only':
        if all_domains: #if not empty
            keys = []
            length = []
            for key in all_domains.keys(): #make main red nodes
                keys.append(key)
                length.append(len(all_domains[key]))
            for src, size in zip(keys, length):
                got_net.add_node(src,src, size=13+math.log2(int(size)**5), title=src, color='red')

            for src, edges in all_domains.items(): #make other nodes
                got_net.add_node(src, src, size=len(edges)*5, title=src, color='green')
                for dst in edges:
                    got_net.add_node(dst, dst, title=dst, color='white')
                    got_net.add_edge(src, dst)
                    print(f'New edge: {src}: {dst}')

            got_net.set_options('''
            var options = {
                "nodes": {
                    "borderWidthSelected": 3,
                    "font": {
                        "color": "rgba(117,117,117,1)",
                        "size": 24,
                        "face": "arial",
                        "strokeWidth": 1
                    },
                    "size": 13
                }
            }
            ''')
            
            initial_link = urlparse(initial_link).netloc #name graph as domain name
            if initial_link.split('.')[0] == 'www': 
                initial_link = initial_link[4:]
            
            got_net.save_graph('graphs/'+initial_link+'.html')
            got_net.save_graph('graphs/graphme.html')
            return True #return that everything is ok

        else: #if list is empty
            main.st.warning('Site has anti-parsing system. Choose another one.')
            return False