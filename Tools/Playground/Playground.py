from flask import Flask, request, render_template
import rdflib
from rdflib import Graph, Namespace, Literal, RDF
import pyshacl
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString


app = Flask(__name__)

# Set the path to the desired standard directory. 
directory_path = "C:/Users/Administrator/Documents/Branches/"

# namespace declaration
html = Namespace("https://data.rijksfinancien.nl/html/model/def/")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
doc = Namespace("http://www.example.org/document/")


# Function to read a graph (as a string) from a file 
def readStringFromFile(file_path):
    # Open each file in read mode
    with open(file_path, 'r', encoding='utf-8') as file:
            # Read the content of the file and append it to the existing string
            file_content = file.read()
    return file_content

html_vocabulary = readStringFromFile(directory_path + "htmlvoc/Specification/html - core.ttl")
example_rdf_code = """### Enter here your RDF-code (turtle-format). 
                           
### For example: \n""" + readStringFromFile(directory_path + "htmlvoc/Examples/HTML-table-template-example.ttl")
example_html_code = """<!-- Enter here your HTML-code. 

For example: --> \n""" + readStringFromFile(directory_path + "htmlvoc/Examples/HTML-table-template-example.html")

def generate_element_id(element):
    # generate an identifier for an element in the xml
    parent_string = ""
    for parent in element.parents:
        parent_sibling_count = 0
        for parent_sibling in parent.previous_siblings:    
            parent_sibling_count = parent_sibling_count + 1
        horizontal_parental_index = parent_sibling_count
        if parent.name:
            parent_string = parent_string + str(horizontal_parental_index)
        else:
            parent_string = parent_string + "0"
        
    count_sibling = 0
    for sibling in element.previous_siblings:    
        count_sibling = count_sibling + 1
    horizontal_index = count_sibling
    
    element_id = f"{parent_string}/{horizontal_index}" 
    
    return element_id.replace("[document]/","")

def iteratePyShacl(shaclgraph, serializable_graph):
        
        # call PyShacl engine and apply the html vocabulary to the serializable html document
        pyshacl.validate(
        data_graph=serializable_graph,
        shacl_graph=shaclgraph,
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
            print ("ask result = ", result)
            if result == False:
                return iteratePyShacl(shaclgraph, serializable_graph)
         
            else:
                htmlQuery = serializable_graph.query('''
                   
               PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
               PREFIX html: <https://data.rijksfinancien.nl/html/model/def/>
               PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

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
    g = rdflib.Graph().parse(data=text , format="turtle")
    # Zet de RDF-triples om naar een string
    triples = g.serialize(format='turtle')
    serializable_graph_string = html_vocabulary + triples
    serializable_graph = rdflib.Graph().parse(data=serializable_graph_string , format="turtle")
    html_fragment = iteratePyShacl(html_vocabulary, serializable_graph)
    print("HTML fragment =", html_fragment)
    return render_template('index.html', htmlOutput=html_fragment, htmlRawOutput=html_fragment, rdfInput=text)

@app.route('/convert2RDF', methods=['POST'])
def convert_to_rdf():
        htmlInput = request.form['html']
        # initialize graph
        g = Graph(bind_namespaces="rdflib")
              
        g.bind("html", html)
        g.bind("rdf", rdf)
        g.bind("rdfs", rdfs)
        g.bind("doc", doc)

        # fill graph with html vocabulary
        html_graph = Graph().parse(directory_path+"htmlvoc/Specification/html - core.ttl" , format="ttl")

        # string for query to establish IRI of a 'tag' HTML element
        tagquerystring = '''
            
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix html: <https://data.rijksfinancien.nl/html/model/def/>

        select ?element_IRI where {
          ?element_IRI html:tag ?tag
        }
        '''

        # parse html document
        soup = BeautifulSoup(htmlInput, 'html.parser')

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
                    elif isinstance(child, NavigableString):
                      child_id = str(element.sourceline) + "." + str(element.sourcepos) + "." + str(member_count) # string elements do not have sourceline or sourcepos, hence we look at their parent to establish an id and add the sequence position of the child
                      
                      # write to graph that the parent element has a child with a certain sequence position
                      g.add((doc[element_id], rdf["_" + str(member_count)], doc[child_id]))  
                      
                      # write to graph that the child element is of type TextElement
                      g.add((doc[child_id], RDF.type, html["TextElement"]))
                      
                      # empty content (of type None) in html needs to be converted to empty string
                      if element.string == None: 
                          text_fragment = "" 
                      else:
                          text_fragment = element.string
                      
                      # write string content of the text element to the graph
                      g.add((doc[child_id], html["fragment"], Literal(text_fragment)))

        # return the resulting triples
        triples = g.serialize(format="turtle",normalize=True).split('\n\n\n')
        return render_template('index.html', rdfOutput=triples, htmlInput = htmlInput, htmlRawInput = htmlInput)

@app.route('/')
def index():
    return render_template('index.html', rdfInput=example_rdf_code, htmlRawInput=example_html_code)

if __name__ == '__main__':
    app.run()
