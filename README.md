
# Specification 'htmlvoc'

This is the repository for htmlvoc, the semantic HTML-vocabulary. You're welcome to contribute! 

# Background

The mission of the community group [Semantic HTML-vocabulary](https://www.w3.org/community/htmlvoc/) is to establish a draft standard for a RDF-based representation of the HTML-vocabulary. With the HTML-vocabulary in RDF, any type of an HTML-document can be meaningfully represented, generated and validated using nothing but standard semantic technologies, without any vendor lock-in. In addition, full provenance can be provided for a generated HTML-document, as every atom of the document can be described and semantically enriched, ex ante (RDF) and ex post (Rdfa). For instance, the originating algorithm that calculates a certain budget amount in a governmental HTML-document can be linked to the table cell containing the very value. HTML-documents have a wide variety of use and so has the HTML vocabulary. The HTML-vocabulary can be used to generate 100% correct HTML or xHTML and to validate this. The HTML vocabulary can be used to model the front end of a website or application, whereas the logic behind the front end can be captured in SHACL Advanced Features, making for a full semantic representation and execution of digital infrastructure, without any vendor lock-in. An HTML-document can be generated with full compliance to laws and regulations, as these norms can be linked and applied while using the HTML-vocabulary. With full provenance, an HTML-document can battle fake news and show realtime how certain sensitive data in the document (privacy, security) was derived. The community group will come up with a 0.1 draft specification. This will be input for a future working group within W3C. The community group can make use of the currently available draft specification as developed by the Dutch Ministry of Finance in a working prototype for the Dutch governmental budget cycle. By starting this community group, the Dutch Ministry wants to contribute to an open source based digital infrastructure.

# Introduction

Let us go through the semantic HTML-vocabulary with an example of an ordinary HTML-document.

## Example: an ordinary HTML-document

```
<!DOCTYPE html>
<html>
<head>
    <title>Tutorial Document Example</title>
    <style>
        table {
            width: 70%;
            margin: 0 auto;
            border-collapse: collapse;
        }

        caption {
            text-align: left;
            font-weight: bold;
            padding: 10px;
            background-color: #f2f2f2; /* Light gray */
        }

        th, td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd; /* Light gray border */
        }

        th {
            background-color: #4CAF50; /* Green */
            color: white;
        }
    </style>
</head>
<body>
    <table>
        <caption>Example table</caption>
        <thead>
            <tr>
                <th>banana</th>
                <th>orange</th>
                <th>apple</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>1</td>
                <td>2</td>
                <td>3</td>
            </tr>
            <tr>
                <td>a</td>
                <td>b</td>
                <td>c</td>
            </tr>
        </tbody>
    </table>
</body>
</html>
```

This table is rendered in a browser as follows:

![An example of an HTML-document](/Examples/ExampleTable-HTMLDocument.jpg)

## Expressing the HTML-document in RDF

Now we can represent the very same document in <i>RDF</i> using the HTML-vocabulary. As it is very cumbersome to do so by hand, a <i>HTML2RDF</i> tool is available in this repository that will do exactly that for you. For further information on this tool and other neat tools, scroll down this Readme file.

```
@prefix doc: <http://www.example.org/document/> .
@prefix html: <https://data.rijksfinancien.nl/html/model/def/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

doc:1 a html:Document ;
    rdf:_1 doc:2.0 .

doc:2.0 a html:Html ;
    rdf:_1 doc:2.0.1 ;
    rdf:_2 doc:3.0 ;
    rdf:_3 doc:2.0.3 ;
    rdf:_4 doc:31.0 ;
    rdf:_5 doc:2.0.5 .

doc:2.0.1 a html:TextElement ;
    html:fragment "" .

doc:2.0.3 a html:TextElement ;
    html:fragment "" .

doc:2.0.5 a html:TextElement ;
    html:fragment "" .

doc:3.0 a html:Head ;
    rdf:_1 doc:3.0.1 ;
    rdf:_2 doc:4.4 ;
    rdf:_3 doc:3.0.3 ;
    rdf:_4 doc:5.4 ;
    rdf:_5 doc:3.0.5 .

doc:3.0.1 a html:TextElement ;
    html:fragment "" .

doc:3.0.3 a html:TextElement ;
    html:fragment "" .

doc:3.0.5 a html:TextElement ;
    html:fragment "" .

doc:31.0 a html:Body ;
    rdf:_1 doc:31.0.1 ;
    rdf:_2 doc:32.4 ;
    rdf:_3 doc:31.0.3 .

doc:31.0.1 a html:TextElement ;
    html:fragment "" .

doc:31.0.3 a html:TextElement ;
    html:fragment "" .

doc:32.4 a html:Table ;
    rdf:_1 doc:32.4.1 ;
    rdf:_2 doc:33.8 ;
    rdf:_3 doc:32.4.3 ;
    rdf:_4 doc:34.8 ;
    rdf:_5 doc:32.4.5 ;
    rdf:_6 doc:41.8 ;
    rdf:_7 doc:32.4.7 .

doc:32.4.1 a html:TextElement ;
    html:fragment "" .

doc:32.4.3 a html:TextElement ;
    html:fragment "" .

doc:32.4.5 a html:TextElement ;
    html:fragment "" .

doc:32.4.7 a html:TextElement ;
    html:fragment "" .

doc:33.8 a html:Caption ;
    rdf:_1 doc:33.8.1 .

doc:33.8.1 a html:TextElement ;
    html:fragment "Example table" .

doc:34.8 a html:TableHeader ;
    rdf:_1 doc:34.8.1 ;
    rdf:_2 doc:35.12 ;
    rdf:_3 doc:34.8.3 .

doc:34.8.1 a html:TextElement ;
    html:fragment "" .

doc:34.8.3 a html:TextElement ;
    html:fragment "" .

doc:35.12 a html:DataRow ;
    rdf:_1 doc:35.12.1 ;
    rdf:_2 doc:36.16 ;
    rdf:_3 doc:35.12.3 ;
    rdf:_4 doc:37.16 ;
    rdf:_5 doc:35.12.5 ;
    rdf:_6 doc:38.16 ;
    rdf:_7 doc:35.12.7 .

doc:35.12.1 a html:TextElement ;
    html:fragment "" .

doc:35.12.3 a html:TextElement ;
    html:fragment "" .

doc:35.12.5 a html:TextElement ;
    html:fragment "" .

doc:35.12.7 a html:TextElement ;
    html:fragment "" .

doc:36.16 a html:HeaderCell ;
    rdf:_1 doc:36.16.1 .

doc:36.16.1 a html:TextElement ;
    html:fragment "banana" .

doc:37.16 a html:HeaderCell ;
    rdf:_1 doc:37.16.1 .

doc:37.16.1 a html:TextElement ;
    html:fragment "orange" .

doc:38.16 a html:HeaderCell ;
    rdf:_1 doc:38.16.1 .

doc:38.16.1 a html:TextElement ;
    html:fragment "apple" .

doc:4.4 a html:Title ;
    rdf:_1 doc:4.4.1 .

doc:4.4.1 a html:TextElement ;
    html:fragment "Tutorial Document Example" .

doc:41.8 a html:TableBody ;
    rdf:_1 doc:41.8.1 ;
    rdf:_2 doc:42.12 ;
    rdf:_3 doc:41.8.3 ;
    rdf:_4 doc:47.12 ;
    rdf:_5 doc:41.8.5 .

doc:41.8.1 a html:TextElement ;
    html:fragment "" .

doc:41.8.3 a html:TextElement ;
    html:fragment "" .

doc:41.8.5 a html:TextElement ;
    html:fragment "" .

doc:42.12 a html:DataRow ;
    rdf:_1 doc:42.12.1 ;
    rdf:_2 doc:43.16 ;
    rdf:_3 doc:42.12.3 ;
    rdf:_4 doc:44.16 ;
    rdf:_5 doc:42.12.5 ;
    rdf:_6 doc:45.16 ;
    rdf:_7 doc:42.12.7 .

doc:42.12.1 a html:TextElement ;
    html:fragment "" .

doc:42.12.3 a html:TextElement ;
    html:fragment "" .

doc:42.12.5 a html:TextElement ;
    html:fragment "" .

doc:42.12.7 a html:TextElement ;
    html:fragment "" .

doc:43.16 a html:DataCell ;
    rdf:_1 doc:43.16.1 .

doc:43.16.1 a html:TextElement ;
    html:fragment "1" .

doc:44.16 a html:DataCell ;
    rdf:_1 doc:44.16.1 .

doc:44.16.1 a html:TextElement ;
    html:fragment "2" .

doc:45.16 a html:DataCell ;
    rdf:_1 doc:45.16.1 .

doc:45.16.1 a html:TextElement ;
    html:fragment "3" .

doc:47.12 a html:DataRow ;
    rdf:_1 doc:47.12.1 ;
    rdf:_2 doc:48.16 ;
    rdf:_3 doc:47.12.3 ;
    rdf:_4 doc:49.16 ;
    rdf:_5 doc:47.12.5 ;
    rdf:_6 doc:50.16 ;
    rdf:_7 doc:47.12.7 .

doc:47.12.1 a html:TextElement ;
    html:fragment "" .

doc:47.12.3 a html:TextElement ;
    html:fragment "" .

doc:47.12.5 a html:TextElement ;
    html:fragment "" .

doc:47.12.7 a html:TextElement ;
    html:fragment "" .

doc:48.16 a html:DataCell ;
    rdf:_1 doc:48.16.1 .

doc:48.16.1 a html:TextElement ;
    html:fragment "a" .

doc:49.16 a html:DataCell ;
    rdf:_1 doc:49.16.1 .

doc:49.16.1 a html:TextElement ;
    html:fragment "b" .

doc:5.4 a html:StyleSheet ;
    rdf:_1 doc:5.4.1 .

doc:5.4.1 a html:TextElement ;
    html:fragment """
        able {
            width: 70%;
            margin: 0 auto;
            border-collapse: collapse;
        }

        caption {
            text-align: left;
            font-weight: bold;
            padding: 10px;
            background-color: #f2f2f2; /* Light gray */
        }

        th, td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd; /* Light gray border */
        }

        th {
            background-color: #4CAF50; /* Green */
            color: white;
        }
    """ .

doc:50.16 a html:DataCell ;
    rdf:_1 doc:50.16.1 .

doc:50.16.1 a html:TextElement ;
    html:fragment "c" .
```

Make note on how each element in the HTML-document is identified by a unique identifier, the IRI (Internationalized Resource Identifier). Now we can address each element, or combinations of elements, and say something about them. Either we express meaning (RDF, RDFS, OWL and more), or impose constraints (SHACL) or we can query (SPARQL) them to know more about them.

# Tools

This repository comes with two, fairly primitive, tools to handle HTML-documents and RDF-representations of HTML. Both tools make extensive use of RDFlib.

## HTML2RDF

The tool HTML2RDF is used to read HTML-documents, parse them and then transform them to RDF-based triples. 

This can be used for several reasons; one could want to have better control over information housekeeping within a organisation. By expressing an HTML-document in RDF-based triples, information flows and slices can be controlled at document or atom level (or any level for that matter), depending on your wishes.

Second, with HTML2RDF one can more easily create a RDF-based template for a family of HTML-documents that one has to generate. Having such a RDF-based template, one can inject new information into the template, creating an instantatiated new document.

### How to use HTML2RDF

A. Install all necessary libraries:

	1. pip install os 
	2. pip install bs4
	3. pip install rdflib

B. Place one or more HTML-files in the input folder in htmlvoc\Tools\HTML2RDF\Input. Only ordinary HTML-files can be processed. 

C. Run the script in the command prompt by typing: 

```
python HTML2RDF.py
```

D. Go to the output folder in htmlvoc\Tools\HTML2RDF\Output and grab your Turtle-file(s) (*.ttl). 




## RDF2HTML

The tool RDF2HTML is used to read a RDF-based representation of an HTML-document into a graph and then serialize and save this to an actual HTML-file. 

### How to use RDF2HTML

A. Install all necessary libraries:

	1. pip install os 
	2. pip install bs4
	3. pip install pyshacl
	3. pip install rdflib

B. Place one or more Turtle-files (*.ttl) in the input folder in htmlvoc\Tools\RDF2HTML\Input. A Turtle-file should represent a HTML-document using the HTML-vocabulary from this repository.

C. Run the script in the command prompt by typing: 

```
python RDF2HTML.py
```

D. Go to the output folder in htmlvoc\Tools\RDF2HTML\Output and grab your HTML-file(s). Additionally included are Turtle-file(s) (*.ttl) that contain the serialized the html:fragment properties for the very same HTML-document. 

### Known issues

Currently there are some needed workaround concerning the use of both RDFlib and PyShacl.

1. The generated HTML-code is captured in a graph with datatype xsd:string. Although not inherently incorrect, ideally a fragment of HTML-code would be represented with the more suiting datatype rdf:HTML. The latter unfortunately triggers an issue in a library HTML5Parser that appearantly is called by RDFLib in one way or the other. Hence, we adjusted our vocabulary, specifically the SHACL shapes in which we manipulate the HTML code, and represent html fragments as xsd:string for now.

See https://github.com/RDFLib/rdflib/issues/2475 (Although neatly corrected as much as possible within the scope of RDFlib, the issue remains in an external library HTML5Parser)

2. There is a small issue in RDFlib using double "filter not exists" SPARQL statements. There is elegant workaround and this has been applied to the HTML-vocabulary. In time this workaround may be reversed if the bug has been solved and the community has expressed its wish in doing so.

See https://github.com/RDFLib/rdflib/issues/2484 

3. When a RDF-based representation of an HTML-document contains html attributes that are not yet known in the vocabulary, the generation process to HTML-code skips the element to which the attribute belongs, hence one might miss portions of the document. Solution is to add to the vocabulary. Currently we are working on completing the RDF-representation of all known HTML attributes in the living standard. For custom HTML attributes the same issue and solution applies.

The html_vocabulary on line 79 should then be adjusted: 

```
html_vocabulary = readGraphFromFile(directory_path + "htmlvoc/Specification/html.ttl")
```
To:

```
html_vocabulary = readGraphFromFile(directory_path + "htmlvoc/Specification/html.ttl")

addendum_vocabulary = readGraphFromFile(directory_path + "htmlvoc/Specification/addendum.ttl")

html_vocabulary = html_vocabulary + addendum_vocabulary
```

# Acknowledgements

We would like to thank Iwan Aucamp @RDFlib for his unrelenting support and accomplishments regarding the open source triple store and related services, as well as Ashley Sommers @PyShacl for his work on the important open source implementation of a SHACL engine. 