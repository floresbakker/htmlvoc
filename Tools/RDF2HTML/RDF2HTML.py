# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 19:42:53 2023

@author: Flores Bakker

The HTML generator offers a simple way of serialising a RDF-model of an HTML-document into an actual HTML-file with HTML-code. 
Just place your own RDF-model (in turtle format) in the input directory.

Attention: whenever a custom made html attribute is used (for example 'html:myOwnAttribute' or something), the serialisation will skip the element to which the attribute belongs, unless this attribute is explicitly defined as being rdfs:subPropertyOf html:attribute. 
Only then the SHACL engine can work with this attribute. This rdfs:subPropertyOf relation defining the custom attribute as a subproperty of html:attribute should be added as part of the vocabulary. In the future this will be supported better by this script, for instance with a separate turtle file containg any additionally created custom attributes.


"""
import pyshacl
import rdflib 
import os
rdflib.NORMALIZE_LITERALS = False #see bug https://github.com/RDFLib/rdflib/issues/2475

# Set the path to the desired standard directory. 
directory_path = "C:/Users/Administrator/Documents/Branches/"

# Function to read a graph (as a string) from a file 
def readGraphFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

# Function to write a graph to a file
def writeGraph(graph):
    graph.serialize(destination=directory_path+"/htmlvoc/Tools/RDF2HTML/Output/"+filename_stem+"-serialized.ttl", format="turtle")

# Function to call the PyShacl engine so that a RDF model of an HTML document can be serialized to HTML-code.
def iteratePyShacl(html_vocabulary, serializable_graph):
        
        # call PyShacl engine and apply the HTML vocabulary to the serializable HTML document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=html_vocabulary,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        advanced=True,
        inplace=True,
        inference=None,
        iterate_rules=False, # Not using the iterate rules function of PyShacl as it seems to not be working properly. Instead, offer each new resulting state freshly to PyShacl.
        debug=False,
        )
      
        # Query to know if the document has been fully serialised by testing whether the root has a html:fragment property. If it has, the algorithm has reached the final level of the document.
        resultquery = serializable_graph.query('''
            
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX html: <https://data.rijksfinancien.nl/html/model/def/>
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
html_vocabulary = readGraphFromFile(directory_path + "htmlvoc/Specification/html.ttl")

# loop through any turtle files in the input directory
for filename in os.listdir(directory_path+"htmlvoc/Tools/RDF2HTML/Input"):
    if filename.endswith(".ttl"):
        file_path = os.path.join(directory_path+"htmlvoc/Tools/RDF2HTML/Input", filename)
        
        # Establish the stem of the file name for reuse in newly created files
        filename_stem = os.path.splitext(filename)[0]

        # Get the RDF-model of some HTML document and place it in a string. 
        document_graph = readGraphFromFile(file_path)                  

        # Join the HTML vocabulary and the RDF-model of some HTML document into a string
        serializable_graph_string = html_vocabulary + document_graph

        # Create a graph of the string containing the HTML vocabulary and the RDF-model of some HTML document
        serializable_graph = rdflib.Graph().parse(data=serializable_graph_string , format="ttl")

        # Inform user
        print ("Serialising the html as contained in document '" + filename + "'...")

        # Call the shacl engine with the HTML vocabulary and the document to be serialized
        iteratePyShacl(html_vocabulary, serializable_graph)

        # Prepare a graph to query the serialized document
        serialized_graph = rdflib.Graph().parse(directory_path+"/htmlvoc/Tools/RDF2HTML/Output/"+filename_stem+"-serialized.ttl" , format="ttl")

        # Query to get the resulting fragment of the document
        documentQuery = serialized_graph.query('''
            
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX html: <https://data.rijksfinancien.nl/html/model/def/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        select ?fragment
        WHERE {
          ?document a html:Document ;
                  html:fragment ?fragment.
        }

        ''')   

        # Write serialized html to actual html file
        for result in documentQuery:
            with open(directory_path+"/htmlvoc/Tools/RDF2HTML/Output/"+filename_stem+"-serialized.html", 'w', encoding='utf-8') as file:
               file.write(result.fragment)
               print ("Document is saved to HTML-format as " + filename_stem+"-serialized.html")

    else:
        print ("No turtle file ('*.ttl') detected")

