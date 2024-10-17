# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:40:53 2023

@author: Flores Bakker

The HTML2RDF script offers a simple way of transforming an HTML-document into a representation of the HTML-code in RDF-based triples. Just set your base directory and place there your own HTML-document so that the script can transform this to RDF-format.

"""

from bs4 import BeautifulSoup, Doctype
from bs4.element import Tag, NavigableString, Comment, CData
from rdflib import Graph, Namespace, Literal, RDF
import os

# Get the current working directory in which the HTML2RDF.py file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))

# namespace declaration
doc  = Namespace("http://www.example.org/document/")
dom  = Namespace("http://www.w3.org/DOM/model/def/") 
html = Namespace("https://www.w3.org/html/model/def/")
rdf  = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# function to read a graph (as a string) from a file 
def readGraphFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding = 'utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

def generate_node_id(node):
    # Base case: If there's no parent, return an empty string (root-level element)
    if node.parent is None:
        return "1"

    # Initialize the sibling index for the current element
    sibling_index = 1
    # Count previous siblings (including text and non-element nodes)
    for sibling in node.previous_siblings:
        sibling_index += 1

    # Recursive call: Get the parent's ID
    parent_id = generate_node_id(node.parent)

    # If the parent ID is not empty, append the current element's sibling index
    if parent_id:
        return f"{parent_id}.{sibling_index}"
    else:
        return str(sibling_index)  # This happens at the root level
    
# loop through any html files in the input directory
for filename in os.listdir(directory_path+"/htmlvoc/Tools/HTML2RDF/Input"):
    if filename.endswith(".html"):
        file_path = os.path.join(directory_path+"/htmlvoc/Tools/HTML2RDF/Input", filename)
        
        # Establish the stem of the file name for reuse in newly created files
        filename_stem = os.path.splitext(filename)[0]

        # place the html code in a string
        htmlInput = readGraphFromFile (file_path)

        # initialize graph
        g = Graph()
        g.bind("html", html)
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("doc", doc)
        g.bind("dom", dom)

        # fill graph with html vocabulary
        html_graph = Graph().parse(directory_path+"/htmlvoc/Specification/html - core.ttl" , format="ttl")

        # string for query to establish IRI of a 'tag' HTML element
        tagquerystring = '''
            
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix html: <https://www.w3.org/html/model/def/>

        select ?element where {
          ?element html:tag ?tag
        }
        '''

        # parse html document
        soup = BeautifulSoup(htmlInput, 'html.parser')
        
        document_id = '1'
       
        for item in soup.contents:
          if isinstance(item, Doctype):
             doctype_id = '2'  # Assign a unique identifier for the Doctype
             g.add((doc[document_id], RDF.type, html["Document"]))
             g.add((doc[document_id], rdf["_1"], doc[doctype_id]))
             g.add((doc[doctype_id], RDF.type, html["DocumentType"]))  # Add the doctype as a DocumentType element in your graph
             g.add((doc[doctype_id], html["documentTypeName"], Literal(str(item))))  # Add the doctype content to the graph
             
        # go through each node in the html document
        for node in soup.descendants:
           
           # check if the node is an html element (identified by a tag)
           if isinstance(node, Tag):
               
               # establish unique id for the html element
               node_id = str(node.sourceline) + "." + str(node.sourcepos)
               
               # establish IRI for the html element based on the HTML vocabulary
               elementResult = html_graph.query(tagquerystring, initBindings={"tag" : Literal(node.name)})
               for row in elementResult:
                   htmlELement = row.element
                   
               # add the element to the graph with its unique identifier as IRI and its tag as type
               g.add((doc[node_id], RDF.type, htmlELement))
               
               # add a document node as a container of the HTML-tree
               if node.name == 'html':
                   g.add((doc[document_id], rdf["_2"], doc[node_id]))


                # establish optional attributes of the element       
               for attribute, values in node.attrs.items():
                    # check whether the attribute consists of multiple values (as list)
                    if isinstance(values, list):
                      attribute_value = ' '.join(values)
                    else: # then it must be one value only (a string)
                      attribute_value = values
                
                    # add optional attributes of the element to the graph
                    g.add((doc[node_id], html[attribute], Literal(attribute_value)))

                # go through the direct children of the element
               member_count = 0 # initialize count
               for child in node.children:
                    member_count = member_count + 1 # count the number of direct children, so that we can establish the sequence of appearance of the children within the parent element, through the 'rdf:_x' property between parent and child.
                    
                    # if the child is an html element (as indicated by the tag) get its unique identifier based on sourceline and sourcepos
                    if isinstance(child, Tag):
                      child_id = str(child.sourceline) + "." + str(child.sourcepos)
                      g.add((doc[node_id], rdf["_" + str(member_count)], doc[child_id]))
                      
                    # if the child is an text node, create a unique identifier based on sourceline and sourcepos of its parent and the sequence position of the child within the parent, as the html-parser does not have sourceline and sourcepos available as attributes for text nodes.
                    elif isinstance(child, NavigableString) and not isinstance(child, Comment):
                      child_id = str(node.sourceline) + "." + str(node.sourcepos) + "." + str(member_count) # string elements do not have sourceline or sourcepos, hence we look at their parent to establish an id and add the sequence position of the child
                      
                      # write to graph that the parent element has a child with a certain sequence position
                      g.add((doc[node_id], rdf["_" + str(member_count)], doc[child_id]))  
                      
                      # write to graph that the child node is of type Text
                      g.add((doc[child_id], RDF.type, html["Text"]))
                      
                      # Get the text content of the current text node and preserve exact indentation and whitespaces
                      text_content = str(child)
                      
                      # write string content of the text node to the graph
                      g.add((doc[child_id], html["fragment"], Literal(text_content)))
                      
                    elif isinstance(child, Comment):
                      child_id = str(node.sourceline) + "." + str(node.sourcepos) + "." + str(member_count) # comment nodes do not have sourceline or sourcepos, hence we look at their parent to establish an id and add the sequence position of the child
                      child_text_id = child_id + '-text'
                      # write to graph that the parent node has a child with a certain sequence position
                      g.add((doc[node_id], rdf["_" + str(member_count)], doc[child_id]))  
                      
                      # write to graph that the child node is of type Comment
                      g.add((doc[child_id], RDF.type, html["Comment"]))
                      
                      # write to graph that the child node 'Comment' has a child 'Text'
                      g.add((doc[child_id], rdf["_1"], doc[child_text_id]))
                      
                      # write to graph that the grand child node is of type Text
                      g.add((doc[child_text_id], RDF.type, html["Text"]))
                      
                      # Get the text content of the current text node and preserve exact indentation and whitespaces
                      text_content = str(child)
                      
                      # write string content of the text node to the graph
                      g.add((doc[child_text_id], html["fragment"], Literal(text_content)))
                      
                    elif isinstance(child, CData):
                      child_id = str(node.sourceline) + "." + str(node.sourcepos) + "." + str(member_count) # CDATA nodes do not have sourceline or sourcepos, hence we look at their parent to establish an id and add the sequence position of the child
                      child_text_id = child_id + '-text'
                      # write to graph that the parent node has a child with a certain sequence position
                      g.add((doc[node_id], rdf["_" + str(member_count)], doc[child_id]))  
                        
                      # write to graph that the child node is of type Text
                      g.add((doc[child_id], RDF.type, html["CDATA"]))
                      
                      # write to graph that the child node 'CDATA' has a child node 'Text'
                      g.add((doc[child_id], rdf["_1"], doc[child_text_id]))
                        
                      # write to graph that the grand child node is of type Text
                      g.add((doc[child_text_id], RDF.type, html["Text"]))
                        
                      # Get the text content of the current text node and preserve exact indentation and whitespaces
                      text_content = str(child)
                        
                      # write string content of the text node to the graph
                      g.add((doc[child_text_id], html["fragment"], Literal(text_content)))

        # write the resulting graph to file
        g.serialize(destination=directory_path+"/htmlvoc/Tools/HTML2RDF/Output/" + filename_stem + "-parsed.ttl", format="turtle")
        
        print ("HTML file ", filename," is succesfullly transformed to file ", filename_stem + "-parsed.ttl in Turtle format.")
    else: 
        print ('Warning: file in directory "input" is no HTML file and cannot be parsed.')

