# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 18:40:53 2023

@author: Flores Bakker

The HTML2RDF script offers a simple way of transforming an HTML-document into a representation of the HTML-code in RDF-based triples. Just set your base directory and place there your own HTML-document so that the script can transform this to RDF-format.

"""

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment, CData
from rdflib import Graph, Namespace, Literal, RDF, Dataset
import os

try:
    # Command prompt execution: current directory is based on location of playground.py file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory_path = os.path.abspath(os.path.join(current_dir, '..', '..'))

except NameError:
    # Python IDE exectution: current directory is based on the IDE working directory in Spyder, Jupyter or iPython.
    # PLEASE NOTE: Set working directory in IDE to OntoMermaid root dir.
    current_dir = os.getcwd()
    directory_path  = os.path.abspath(os.path.join(current_dir))

# namespace declaration
html = Namespace("https://www.w3.org/html/model/def/")
rdf  = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
doc  = Namespace("http://www.example.org/document/")

# function to read a graph (as a string) from a file 
def readGraphFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding = 'utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

# loop through any html files in the input directory
for filename in os.listdir(directory_path+"/tools/HTML2RDF/input"):
    if filename.endswith(".html"):
        file_path = os.path.join(directory_path+"/tools/HTML2RDF/input", filename)
        
        # Establish the stem of the file name for reuse in newly created files
        filename_stem = os.path.splitext(filename)[0]

        # place the html code in a string
        html_doc = readGraphFromFile (file_path)

        # initialize graph
        g = Graph()
        g.bind("html", html)
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("doc", doc)

        # fill graph with html vocabulary
        html_graph = Dataset(default_union=True)
        html_graph.parse(directory_path+"/specification/html - core.trig" , format="trig")

        # string for query to establish IRI of a 'tag' HTML element
        tagquerystring = '''
            
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix html: <https://www.w3.org/html/model/def/>

        select ?element_IRI where {
          ?element_IRI html:tag ?tag
        }
        '''

        # parse html document
        soup = BeautifulSoup(html_doc, 'html.parser')

        # go through each element in the html document
        for element in soup.descendants:
            
            # check if the element is an html tag element
            if isinstance(element, Tag):
                
                # establish unique id for the html tag element
                element_id = str(element.sourceline) + "." + str(element.sourcepos)
                
                # establish IRI for the tag class based on the HTML vocabulary
                tag_result = html_graph.query(tagquerystring, initBindings={"tag" : Literal(element.name)})
                for row in tag_result:
                    tag_IRI = row.element_IRI
                    
                # add the element to the graph with its unique identifier as IRI and its tag as type
                g.add((doc[element_id], RDF.type, tag_IRI))
                
                # add a document node as a container of the HTML-tree
                if element.name == 'html':
                    document_id = '1'
                    g.add((doc[document_id], RDF.type, html["Document"]))
                    g.add((doc[document_id], rdf["_" + str(document_id)], doc[element_id]))

                # establish optional attributes of the element       
                for attribute, values in element.attrs.items():
                    # check whether the attribute consists of multiple values (as list)
                    if isinstance(values, list):
                      attribute_value = ' '.join(values)
                    else: # then it must be one value only (a string)
                      attribute_value = values
                
                    # add optional attributes of the element to the graph
                    g.add((doc[element_id], html[attribute], Literal(attribute_value)))

                # go through the direct children of the element
                member_count = 0 # initialize count
                for child in element.children:
                    member_count = member_count + 1 # count the number of direct children, so that we can establish the sequence of appearance of the children within the parent element, through the 'rdf:_x' property between parent and child.
                    
                    # if the child is an html tag element get its unique identifier based on sourceline and sourcepos
                    if isinstance(child, Tag):
                      child_id = str(child.sourceline) + "." + str(child.sourcepos)
                      g.add((doc[element_id], rdf["_" + str(member_count)], doc[child_id]))
                      
                    # if the child is an text element, create a unique identifier based on sourceline and sourcepos of its parent and the sequence position of the child within the parent, as the html-parser does not have sourceline and sourcepos available as attributes for text elements.
                    elif isinstance(child, NavigableString) and not isinstance(child, Comment):
                      child_id = str(element.sourceline) + "." + str(element.sourcepos) + "." + str(member_count) # string elements do not have sourceline or sourcepos, hence we look at their parent to establish an id and add the sequence position of the child
                      
                      # write to graph that the parent element has a child with a certain sequence position
                      g.add((doc[element_id], rdf["_" + str(member_count)], doc[child_id]))  
                      
                      # write to graph that the child element is of type TextElement
                      g.add((doc[child_id], RDF.type, html["Text"]))
                      
                      # Get the text content of the current text element and preserve exact indentation and whitespaces
                      text_content = str(child)
                      
                      # write string content of the text element to the graph
                      g.add((doc[child_id], html["fragment"], Literal(text_content)))
                      
                    elif isinstance(child, Comment):
                      child_id = str(element.sourceline) + "." + str(element.sourcepos) + "." + str(member_count) # string elements do not have sourceline or sourcepos, hence we look at their parent to establish an id and add the sequence position of the child
                      child_text_id = child_id + '-text'
                      # write to graph that the parent element has a child with a certain sequence position
                      g.add((doc[element_id], rdf["_" + str(member_count)], doc[child_id]))  
                      
                      # write to graph that the child element is of type TextElement
                      g.add((doc[child_id], RDF.type, html["Comment"]))
                      
                      # write to graph that the child element 'Comment' has a child 'TextElement''
                      g.add((doc[child_id], rdf["_1"], doc[child_text_id]))
                      
                      # write to graph that the grand child element is of type TextElement
                      g.add((doc[child_text_id], RDF.type, html["Text"]))
                      
                      # Get the text content of the current text element and preserve exact indentation and whitespaces
                      text_content = str(child)
                      
                      # write string content of the text element to the graph
                      g.add((doc[child_text_id], html["fragment"], Literal(text_content)))
                      
                    elif isinstance(child, CData):
                      child_id = str(element.sourceline) + "." + str(element.sourcepos) + "." + str(member_count) # string elements do not have sourceline or sourcepos, hence we look at their parent to establish an id and add the sequence position of the child
                      child_text_id = child_id + '-text'
                      # write to graph that the parent element has a child with a certain sequence position
                      g.add((doc[element_id], rdf["_" + str(member_count)], doc[child_id]))  
                        
                      # write to graph that the child element is of type TextElement
                      g.add((doc[child_id], RDF.type, html["CDATA"]))
                      
                      # write to graph that the child element 'CDATA' has a child 'TextElement''
                      g.add((doc[child_id], rdf["_1"], doc[child_text_id]))
                        
                      # write to graph that the grand child element is of type TextElement
                      g.add((doc[child_text_id], RDF.type, html["Text"]))
                        
                      # Get the text content of the current text element and preserve exact indentation and whitespaces
                      text_content = str(child)
                        
                      # write string content of the text element to the graph
                      g.add((doc[child_text_id], html["fragment"], Literal(text_content)))

        # write the resulting graph to file
        g.serialize(destination=directory_path+"/tools/HTML2RDF/output/" + filename_stem + "-parsed.trig", format="trig")
        
        print ("HTML file ", filename," is succesfullly transformed to file ", filename_stem + "-parsed.trig in Trig format.")
    else: 
        print ('Warning: file in directory "input" is no HTML file and cannot be parsed.')

