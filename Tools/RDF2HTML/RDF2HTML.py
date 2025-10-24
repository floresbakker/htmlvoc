# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 19:42:53 2023

@author: Flores Bakker

The HTML generator offers a simple way of serialising a RDF-model of an HTML-document into an actual HTML-file with HTML-code. 
Just place your own RDF-model (in trig format) in the input directory.

Attention: whenever a custom made html attribute is used (for example 'html:myOwnAttribute' or something), the serialisation will skip the element to which the attribute belongs, unless this attribute is explicitly defined as being rdfs:subPropertyOf html:attribute. 
Only then the SHACL engine can work with this attribute. This rdfs:subPropertyOf relation defining the custom attribute as a subproperty of html:attribute should be added as part of the vocabulary. In the future this will be supported better by this script, for instance with a separate "*.trig"-file containg any additionally created custom attributes.


"""
import pyshacl
import rdflib 
from rdflib import Dataset 
import os

# Get the current working directory in which the RDF2HTML.py file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir))

# Function to read a graph (as a string) from a file 
def readGraphFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

# Function to write a graph to a file
def writeGraph(graph):
    graph.serialize(destination=directory_path+"/tools/RDF2HTML/output/"+filename_stem+"-serialized.trig", format="trig")

# Function to call the PyShacl engine so that a RDF model of an HTML document can be serialized to HTML-code.
def iteratePyShacl(html_vocabulary, serializable_graph):
        
        # call PyShacl engine and apply the HTML vocabulary to the serializable HTML document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=html_vocabulary,
        data_graph_format="trig",
        shacl_graph_format="trig",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
      
        # Query to know if the document has been fully serialised by testing whether the root has a html:fragment property. If it has, the algorithm has reached the final level of the document.
        resultquery = serializable_graph.query('''
            
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX html: <https://www.w3.org/html/model/def/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        ASK 
        WHERE {
          ?document a html:Document ;
                  html:fragment ?fragment.
        }

        ''')   

        # Check whether another iteration is needed. If the html root of the document contains a html:fragment statement then the serialisation is considered done.
        for result in resultquery:
            if result == False:
                writeGraph(serializable_graph)
                iteratePyShacl(html_vocabulary, serializable_graph)
            else: 
                print ("Document is serialised.")
                writeGraph(serializable_graph)
             

# Get the HTML vocabulary and place it in a string
html_vocabulary = readGraphFromFile(directory_path + "/specification/html - core.trig")
dom_vocabulary = readGraphFromFile(directory_path + "/specification/dom - core.trig")
vocabulary = dom_vocabulary + '\n\n' + html_vocabulary


# Collect all .trig files in the directory
trig_files = [f for f in os.listdir(directory_path+"/tools/RDF2HTML/input") if f.endswith(".trig")]

# Warn only if there are none
if not trig_files:
    print("⚠️  No trig file ('*.trig') detected in the input directory.")
else:
    # loop through any trig files in the input directory
    for filename in trig_files:
        if filename.endswith(".trig"):
            file_path = os.path.join(directory_path+"/tools/RDF2HTML/input", filename)
            
            # Establish the stem of the file name for reuse in newly created files
            filename_stem = os.path.splitext(filename)[0]
    
            # Get the RDF-model of some HTML document and place it in a string. 
            document_graph = readGraphFromFile(file_path)                  
    
            # Join the HTML vocabulary and the RDF-model of some HTML document into a string
            serializable_string = vocabulary + '\n\n'+ document_graph
    
            # Create a graph of the string containing the HTML vocabulary and the RDF-model of some HTML document
            serializable_graph = Dataset(default_union=True)
            serializable_graph.parse(data=serializable_string, format="trig")
    
            # Inform user
            print ("Serialising the html as contained in document '" + filename + "'...")
    
            # Call the shacl engine with the HTML vocabulary and the document to be serialized
            iteratePyShacl(html_vocabulary, serializable_graph)
    
            # Prepare a graph to query the serialized document
            serialized_graph = rdflib.Graph().parse(directory_path+"/tools/RDF2HTML/output/"+filename_stem+"-serialized.trig" , format="trig")
    
            # Query to get the resulting fragment of the document
            documentQuery = serialized_graph.query('''
                
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX html: <https://www.w3.org/html/model/def/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
            select ?fragment
            WHERE {
              ?document a html:Document ;
                      html:fragment ?fragment.
            }
    
            ''')   
    
            # Write serialized html to actual html file
            for result in documentQuery:
                with open(directory_path+"/tools/RDF2HTML/output/"+filename_stem+"-serialized.html", 'w', encoding='utf-8') as file:
                   file.write(result.fragment)
                   print ("Document is saved to HTML-format as " + filename_stem+"-serialized.html")


