from flask import Flask, request, render_template, url_for
import rdflib
from rdflib import Graph, Namespace, Literal, RDF, Dataset
import pyshacl
from bs4 import BeautifulSoup, Doctype
from bs4.element import Tag, NavigableString, Comment, CData
import os

app = Flask(__name__, template_folder='tools/playground/templates', static_folder='tools/playground/static')


# Get the current working directory in which the Playground.py file is located.
current_dir = os.getcwd()

# Set the path to the desired standard directory. 
directory_path = os.path.abspath(os.path.join(current_dir))

# namespace declaration
doc  = Namespace("http://www.example.org/document/")
dom  = Namespace("http://www.w3.org/DOM/model/def/") 
html = Namespace("https://www.w3.org/html/model/def/")
rdf  = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Function to read a graph (as a string) from a file 
def readStringFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

html_vocabulary = readStringFromFile(directory_path + "/specification/html - core.trig")
dom_vocabulary = readStringFromFile(directory_path + "/specification/dom - core.trig")
example_rdf_code = """### Enter here your RDF-code (turtle-format). 
                           
### For example: \n""" + readStringFromFile(directory_path + "/examples/HTML-table-template-example.ttl")
example_html_code = """<!-- Enter here your HTML-code. 

For example: --> \n""" + readStringFromFile(directory_path + "/examples/HTML-table-template-example.html")

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

def iteratePyShacl(shaclgraph, serializable_graph):
        
        # call PyShacl engine and apply the html vocabulary to the serializable html document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=shaclgraph,
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
            
       prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
       prefix html: <https://www.w3.org/html/model/def/>
       prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

       ASK 
       WHERE {
         ?document a html:Document ;
                 html:fragment ?fragment.
       }
        ''')   

        # Check whether another iteration is needed. If the html root of the document contains a html:fragment statement then the serialisation is considered done.
        for result in resultquery:
            print ("ask result = ", result)
            if result == False:
                return iteratePyShacl(shaclgraph, serializable_graph)
         
            else:
                htmlQuery = serializable_graph.query('''
                   
               prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               prefix html: <https://www.w3.org/html/model/def/>
               prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

               select ?fragment
               WHERE {
                 ?document a html:Document ;
                         html:fragment ?fragment.
               }

               ''')   

         
                for html in htmlQuery:
                    print ("html.fragment = ", html.fragment)
                    return html.fragment

@app.route('/convert2HTML', methods=['POST'])
def convert_to_html():
    text = request.form['rdf']   
    g = rdflib.Graph().parse(data=text , format="trig")
    # Zet de RDF-triples om naar een string
    triples = g.serialize(format='trig')
    serializable_graph_string = html_vocabulary + '\n' + dom_vocabulary + '\n' + triples
    serializable_graph = Dataset(default_union=True)
    serializable_graph.parse(data=serializable_graph_string , format="trig")
    html_fragment = iteratePyShacl(html_vocabulary, serializable_graph)
    filepath = directory_path+"/tools/playground/static/output.html"
    src_filepath = url_for('static', filename='output.html')
    with open(filepath, 'w', encoding='utf-8') as file:
       file.write(html_fragment)
    return render_template('index.html', htmlOutput='<iframe src='+ src_filepath + ' width="100%" height="600"></iframe>', htmlRawOutput=html_fragment, rdfInput=text)

@app.route('/convert2RDF', methods=['POST'])
def convert_to_rdf():
        htmlInput = request.form['html']
        # initialize graph
        g = Graph(bind_namespaces="rdflib")
              
        g.bind("html", html)
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("doc", doc)
        g.bind("dom", dom)

        # fill graph with html vocabulary
        html_graph = Dataset(default_union=True)
        html_graph.parse(directory_path+"/specification/html - core.trig" , format="trig")

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
        document_id = '1.0'
        
        for item in soup.contents:
          if isinstance(item, Doctype):
              doctype_id = '1.1'  # Assign a unique identifier for the Doctype
              g.add((doc[document_id], RDF.type, html["Document"]))
              g.add((doc[document_id], rdf["_1"], doc[doctype_id]))
              g.add((doc[doctype_id], RDF.type, html["DocumentType"]))  # Add the doctype as a DocumentType element in your graph
              g.add((doc[doctype_id], html["documentTypeName"], Literal(str(item))))  # Add the doctype content to the graph
              
        # go through each node in the html document
        for node in soup.descendants:
            
            # check if the node is an html element (identified by a tag)
            if isinstance(node, Tag):
                
                # establish unique id for the html element
                node_id = generate_node_id (node)
                
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
                      child_id = generate_node_id(child)
                      g.add((doc[node_id], rdf["_" + str(member_count)], doc[child_id]))
                      
                    # if the child is an text node, create a unique identifier based on sourceline and sourcepos of its parent and the sequence position of the child within the parent, as the html-parser does not have sourceline and sourcepos available as attributes for text nodes.
                    elif isinstance(child, NavigableString) and not isinstance(child, Comment):
                      child_id = generate_node_id(child)
                      
                      # write to graph that the parent element has a child with a certain sequence position
                      g.add((doc[node_id], rdf["_" + str(member_count)], doc[child_id]))  
                      
                      # write to graph that the child node is of type Text
                      g.add((doc[child_id], RDF.type, html["Text"]))
                      
                      # Get the text content of the current text node and preserve exact indentation and whitespaces
                      text_content = str(child)
                      
                      # write string content of the text node to the graph
                      g.add((doc[child_id], html["fragment"], Literal(text_content)))
                      
                    elif isinstance(child, Comment):
                      child_id = generate_node_id(child)
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
                      child_id = generate_node_id(child)
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

        # return the resulting triples
        triples = g.serialize(format="turtle",normalize=True).split('\n\n\n')
        filepath = directory_path+"/tools/playground/static/input.html"
        src_filepath = url_for('static', filename='input.html')
        with open(filepath, 'w', encoding='utf-8') as file:
           file.write(htmlInput)
        return render_template('index.html', rdfOutput=triples, htmlInput='<iframe src='+ src_filepath + ' width="100%" height="600"></iframe>', htmlRawInput = htmlInput)

@app.route('/output')
def output():
    return render_template('output.html')

@app.route('/')
def index():
    return render_template('index.html', rdfInput=example_rdf_code, htmlRawInput=example_html_code)

if __name__ == '__main__':
    app.run()