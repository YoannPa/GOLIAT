import sys
import re
import copy
import numpy as npry
import json 
import random
import networkx as nx
import pandas as pd
import BINARIES.module1 as module1
from py2cytoscape.data.cynetwork import CyNetwork
from py2cytoscape.data.cyrest_client import CyRestClient
from py2cytoscape.data.style import StyleUtil
import py2cytoscape.util.cytoscapejs as cyjs
import py2cytoscape.cytoscapejs as renderer
from IPython.display import display
from IPython.display import Image

print ('My Python Version = ' + sys.version)

def CallCytoscape(nomfichiersorti,path,relation):#Fonction qui cree le fichier "DataCytoscape_" que cytoscape peux lire.
    dico_go=module1.Dico_go()
    dico_go.remplirDico('DATA/go.obo')
    dico=dico_go.GetRelationP(relation)
    Tableau_cyto={}
    Tableau_Goslim_proche=[]
    AllGoslim=[]
    TabSortie=[]
    File = open(nomfichiersorti, "r")
    File.readline()
    for line in File :#lecture du fichier "Output"
        line=line.rstrip()
        tmp=line.split(";")
        if tmp[2]!="old GO":
            if tmp[2]!="" :
                print(tmp[2])
                Tableau_Goslim_proche.append(tmp[2])
                Tableau_cyto[tmp[0]]=tmp[2]
    File.close()
    nameFile="DataCytoscape_"+relation+".csv"
    FileCyto=open(nameFile, "w")
    #FileCyto.write("source"+";"+"interaction"+";"+"target"+";"+"ontology"+"\n")
    for keys in Tableau_cyto :
        FileCyto.write(keys+";"+"gene-go"+";"+ Tableau_cyto[keys]+";"+dico_go.getOntology(keys)+"\n")
    compteur=0
    for go in Tableau_Goslim_proche :
        tab=[]
        TabSortie.extend(getAncestorsCytoscape(go, dico,tab))#Elle renvoie des choses de tailles variables
    TabSortie=set(TabSortie)
    for couple in TabSortie :
        if couple:
            tmp=couple.split(";")
            FileCyto.write(tmp[0]+";"+"go-go"+";"+tmp[1]+";"+dico_go.getOntology(tmp[0])+"\n")
    FileCyto.close()
    CreateNetWork(nameFile)#Creation de la session cytoscape

def getAncestorsCytoscape(goid, terms,tab,niveau=1):#Fonction qui fait les relations parents entre le GOslim proche et les GO ancestraux
    couple=""
    tab=tab
    nom=str(niveau)+"_"+goid
    recursiveArray = [nom]
    if goid in terms :
        parents = terms[goid]
        if len(parents) > 0:
            for parent in parents:
                recursiveArray.extend(getAncestorsCytoscape(parent, terms, tab,niveau+1))
                couple=parent+";"+goid
                tab.append(couple)
    return tab

def CreateNetWork (nameFile):#Fonction qui cree une session Cytoscape avec les donnees du fichier "DataCytoscape_"
    # Create py2cytoscape client
    cy = CyRestClient()
    # Reset
    cy.session.delete()
    # From a simple text table
    df_from_sif = pd.read_csv(nameFile, names=['source', 'interaction','target','ontology'], sep=';')
    #print(df_from_sif.head())
    # By default, it uses 'source' for source node column, 'target' for target node column, and 'interaction' for interaction
    Go_network = cy.network.create_from_dataframe(df_from_sif, name='GO interaction ! Project GOLIAT')
    #print("network id : ",Go_network.get_id())
    # Create columns
    Go_network.create_node_column(name='ontology', data_type='String')
    # Now update existing node table with the data frame above.
    Go_network.update_node_table(df=df_from_sif, network_key_col='ontology' , data_key_col='ontology')
    # Create a new style
    style1 = cy.style.create('GO_GOLIAT_style')
    new_defaults = {
    # Node defaults
    'NODE_FILL_COLOR': '#eeeeff',
    'NODE_SIZE': 20,
    'NODE_BORDER_WIDTH': 0,
    'NODE_TRANSPARENCY': 120,
    'NODE_LABEL_COLOR': 'white',
    # Edge defaults
    'EDGE_WIDTH': 3,
    'EDGE_STROKE_UNSELECTED_PAINT': '#aaaaaa',
    'EDGE_LINE_TYPE': 'LONG_DASH',
    'EDGE_TRANSPARENCY': 120,
    # Network defaults
    'NETWORK_BACKGROUND_PAINT': 'black'
    }
    # Update
    style1.update_defaults(new_defaults)
    # Apply the new style
    cy.style.apply(style1, Go_network)
    # Get SUID of all nodes
    target_edges = Go_network.get_edges()
    target_nodes = Go_network.get_nodes()
    # Get views for a network: Cytoscape "may" have multiple views, and that's why it returns list instead of an object.
    view_id_list = Go_network.get_views()
    # The "format" option specify the return type.
    view1 = Go_network.get_view(view_id_list[0], format='view')
    # Assign key-value pair.  For this example, node SUID to color.
    def get_color_dict(node_ids):
        new_values = {}
        for n in node_ids:
            source=Go_network.get_node_value(id=n, column='name')
            if re.search(b'GO:',source) is None:
                new_values[n] = '#F00000'
            if re.search(b'GO:0003674',source) is not None:
                new_values[n]= '#20F300'
            if re.search(b'GO:0008150',source) is not None:
                new_values[n]= '#20F300'
            if re.search(b'GO:0005575',source) is not None:
                new_values[n]= '#20F300'
        return new_values

    def get_shape_dict(node_ids):
        new_values = {}
        for n in node_ids:
            source=Go_network.get_node_value(id=n, column='name')
            if re.search(b'GO:',source) is None:
                new_values[n] = 'Ellipse'
            if re.search(b'GO:0003674',source) is not None:
                new_values[n]= 'Diamond'
            if re.search(b'GO:0008150',source) is not None:
                new_values[n]= 'Diamond'
            if re.search(b'GO:0005575',source) is not None:
                new_values[n]= 'Diamond'
        return new_values
    
    def get_width_dict(node_ids):
        new_values = {}
        for n in node_ids:
            source=Go_network.get_node_value(id=n, column='name')
            if re.search(b'GO:0003674',source) is not None:
                new_values[n]= 80
            if re.search(b'GO:0008150',source) is not None:
                new_values[n]= 80
            if re.search(b'GO:0005575',source) is not None:
                new_values[n]= 80
        return new_values
    
    def get_height_dict(node_ids):
        new_values = {}
        for n in node_ids:
            source=Go_network.get_node_value(id=n, column='name')
            if re.search(b'GO:0003674',source) is not None:
                new_values[n]= 80
            if re.search(b'GO:0008150',source) is not None:
                new_values[n]= 80
            if re.search(b'GO:0005575',source) is not None:
                new_values[n]= 80
        return new_values
    
    new_values_color = get_color_dict(target_nodes)
    new_values_shape = get_shape_dict(target_nodes)
    new_values_width = get_width_dict(target_nodes)
    new_values_height = get_width_dict(target_nodes)
    # Set new values for a set of nodes.  In this case, all nodes in the network
    view1.update_node_views(visual_property='NODE_FILL_COLOR', values=new_values_color)
    view1.update_node_views(visual_property='NODE_SHAPE', values=new_values_shape)
    view1.update_node_views(visual_property='NODE_WIDTH', values=new_values_width)
    view1.update_node_views(visual_property='NODE_HEIGHT', values=new_values_height)