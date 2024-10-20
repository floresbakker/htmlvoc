
# Specification 'htmlvoc'

This is the repository for htmlvoc, the semantic HTML-vocabulary. You're welcome to contribute! 

# Status

Stable, but no release yet. Work in progress together with the community group [Semantic HTML-vocabulary](https://www.w3.org/community/htmlvoc/). We aim for a preliminary release in the end of 2024, together with a draft report on the vocabulary.

# Background

The mission of the community group [Semantic HTML-vocabulary](https://www.w3.org/community/htmlvoc/) is to establish a draft standard for a RDF-based representation of the HTML living standard. HTML documents can thus be represented, queried, generated, validated, analysed, transformed and reused as semantic objects themselves. In addition, full provenance can be provided for a generated HTML-document, as every atom of the document can be described and semantically enriched, ex ante (RDF) and ex post (Rdfa). For instance, the originating algorithm that calculates a certain budget amount in a governmental HTML-document can be linked to the table cell containing the very value. HTML-documents have a wide variety of use and so has the HTML vocabulary. The HTML vocabulary can be used to generate 100% correct HTML or xHTML and to validate this. The HTML vocabulary can be used to model the front end of a website or application, whereas the logic behind the front end can be captured in SHACL Advanced Features, making for a full semantic representation and execution of digital infrastructure, without any vendor lock-in. An HTML-document can be generated with full compliance to laws and regulations, as these norms can be linked and applied while using the HTML vocabulary. With full provenance, an HTML-document can battle fake news and show realtime how certain sensitive data in the document (privacy, security) was derived. The community group will come up with a 0.1 draft specification. This will be input for a future working group within W3C. The community group can make use of the currently available draft specification as developed by the Dutch Ministry of Finance in a working prototype for the Dutch governmental budget cycle. By starting this community group, the Dutch Ministry wants to contribute to an open source based digital infrastructure.

# Introduction

Let us go through the HTML vocabulary with an example of an ordinary HTML-document.

## Example #1: an ordinary HTML-document with a table

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

![An example of an HTML-document](/Examples/ExampleTable-HTMLDocument.JPG)

## Expressing the HTML-document in RDF

Now we can represent the very same document in <i>RDF</i> using the HTML-vocabulary. As it is very cumbersome to do so by hand, a <i>HTML2RDF</i> tool is available in this repository that will do exactly that for you. For further information on this tool and other neat tools, scroll down this Readme file.

```
prefix doc:  <http://www.example.org/document/> 
prefix html: <https://www.w3.org/html/model/def/> 
prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

doc:1 a html:Document ; 
 rdf:_1 doc:1.0 ;
 rdf:_2 doc:2.0 . 

doc:1.0 a html:DocumentType ;
 html:documentTypeName "html" ;
 html:fragment "<!DOCTYPE html>"^^rdf:HTML .
 
doc:2.0 a html:Html ; 
 rdf:_1 doc:3.0 ; 
 rdf:_2 doc:4.0 .

doc:3.0 a html:Head ; 
 rdf:_1 doc:4.4 ; 
 rdf:_2 doc:5.4 .
 
doc:4.0 a html:Body ;  
 rdf:_1 doc:32.4 .
 
doc:32.4 a html:Table ; 
 rdf:_1 doc:33.8 ; 
 rdf:_2 doc:34.8 ; 
 rdf:_3 doc:41.8 . 

doc:33.8 a html:Caption ; 
 rdf:_1 doc:33.8.1 .

doc:33.8.1 a html:Text ; 
 html:fragment "Example table" . 

doc:34.8 a html:TableHeader ; 
 rdf:_1 doc:35.12 . 

doc:35.12 a html:Row ; 
 rdf:_1 doc:36.16 ; 
 rdf:_2 doc:37.16 ; 
 rdf:_3 doc:38.16 . 

doc:36.16 a html:HeaderCell ; 
 rdf:_1 doc:36.16.1 . 

doc:36.16.1 a html:Text ; 
 html:fragment "banana" .

doc:37.16 a html:HeaderCell ; 
 rdf:_1 doc:37.16.1 .

doc:37.16.1 a html:Text ; 
 html:fragment "orange" .

doc:38.16 a html:HeaderCell ; 
 rdf:_1 doc:38.16.1 .

doc:38.16.1 a html:Text ; 
 html:fragment "apple" .

doc:4.4 a html:Title ; 
 rdf:_1 doc:4.4.1 . 

doc:4.4.1 a html:Text ; 
 html:fragment "Tutorial Document Example" . 

doc:41.8 a html:TableBody ; 
 rdf:_1 doc:42.12 ; 
 rdf:_2 doc:47.12 . 

doc:42.12 a html:Row ; 
 rdf:_1 doc:43.16 ; 
 rdf:_2 doc:44.16 ; 
 rdf:_3 doc:45.16 .

doc:43.16 a html:DataCell ; 
 rdf:_1 doc:43.16.1 .

doc:43.16.1 a html:Text ;
 html:fragment "1" .

doc:44.16 a html:DataCell ; 
 rdf:_1 doc:44.16.1 . 

doc:44.16.1 a html:Text ; 
 html:fragment "2" . 

doc:45.16 a html:DataCell ; 
 rdf:_1 doc:45.16.1 . 

doc:45.16.1 a html:Text ; 
 html:fragment "3" . 

doc:47.12 a html:Row ; 
 rdf:_1 doc:48.16 ; 
 rdf:_2 doc:49.16 ; 
 rdf:_3 doc:50.16 . 

doc:48.16 a html:DataCell ;
 rdf:_1 doc:48.16.1 .

doc:48.16.1 a html:Text ;
 html:fragment "a" . 

doc:49.16 a html:DataCell ;
 rdf:_1 doc:49.16.1 . 

doc:49.16.1 a html:Text ; 
 html:fragment "b" . 

doc:5.4 a html:StyleSheet ; 
 rdf:_1 doc:5.4.1 . 

doc:5.4.1 a html:Text ; 
 html:fragment """\r able {\r width: 70%;\r margin: 0 auto;\r border-collapse: collapse;\r }\r \r caption {\r text-align: left;\r font-weight: bold;\r padding: 10px;\r background-color: #f2f2f2; /* Light gray */\r }\r \r th, td {\r padding: 12px;\r text-align: center;\r border: 1px solid #ddd; /* Light gray border */\r }\r \r th {\r background-color: #4CAF50; /* Green */\r color: white;\r }\r """ . 

doc:50.16 a html:DataCell ;
 rdf:_1 doc:50.16.1 . 

doc:50.16.1 a html:Text ; 
 html:fragment "c" .

doc:50.16 a html:DataCell ;
    rdf:_1 doc:50.16.1 .

doc:50.16.1 a html:Text ;
    html:fragment "c" .
```

Make note on how each element in the HTML-document is identified by a unique identifier, the IRI (Internationalized Resource Identifier). Now we can address each element, or combinations of elements, and say something about them. Either we express meaning (RDF, RDFS, OWL and more), or impose constraints (SHACL) or we can query (SPARQL) them to know more about them.

## Example #2: an application GUI as HTML-document

```
<!DOCTYPE html>
<html>
    <head>
        <title>
        </title>
        <style>body {font-family: Arial, Helvetica, sans-serif; background-color: black; } * {box-sizing: border-box;} /* Add padding to containers */.container {padding: 16px; background-color: white;} /* Full-width input fields */ input[type=text], input[type=password] {width: 100%; padding: 15px;  margin: 5px 0 22px 0; display: inline-block; border: none;  background: #f1f1f1;} input[type=text]:focus, input[type=password]:focus {  background-color: #ddd;  outline: none;} /* Overwrite default styles of hr */ hr {   border: 1px solid #f1f1f1;   margin-bottom: 25px;} /* Set a style for the submit button */ .registerbtn {   background-color: #04AA6D;   color: white;   padding: 16px 20px;   margin: 8px 0;   border:  none;  cursor: pointer;   width: 100%;   opacity: 0.9; } .registerbtn:hover {  opacity: 1;} /* Add a blue text color to links */ a {  color: dodgerblue;} /* Set a grey background color and center the text of the "sign in" section */ .signin {  background-color: #f1f1f1;  text-align: center;}
        </style>
        <meta http-equiv="Content-Type" charset="utf-8">
    </head>
    <body>
        <form action="action_page.php">
            <div class="container">
                <h1>Register</h1>
                <p>Please fill in this form to create an account.</p>
                <hr>
                <label for="email">
                   <b>email</b>
                </label>
                <input id="email" name="email" placeholder="Enter Email" required="true" type="text">
                   <label for="psw">
                      <b>Password</b>
                   </label>
                 <input id="psw" name="psw" placeholder="Enter Password" required="true" type="password">
                    <label for="psw-repeat">
                       <b>Repeat Password</b>
                    </label>
                 <input id="psw-repeat" name="psw-repeat" placeholder="Repeat Password" required="true" type="password">
                 <hr>
                 <p>By creating an account you agree to our 
                   <a href="#">Terms & Privacy</a>.
                  </p>
                  <button class="registerbtn" type="submit">Register</button>
             </div>
             <div class="container signin">
                <p>Already have an account?
                    <a href="#">Sign in</a>.
                </p>
            </div>
        </form>
    </body>
</html>
```

This GUI with forms is rendered in a browser as follows:

![An example of an HTML-document with forms](/Examples/ExampleGUI-HTMLDocument.JPG)

## Again expressing the HTML-document in RDF


```
prefix doc:  <http://www.example.org/document/> 
prefix html: <https://www.w3.org/html/model/def/> 
prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

doc:1 a html:Document ;
    rdf:_1 doc:1.10 ;
    rdf:_2 doc:1.15 .

doc:1.10 a html:DocumentType ;
    html:documentTypeName "html" .

doc:1.1058 a html:Meta ;
    html:charset "utf-8" ;
    html:http-equiv "Content-Type" .

doc:1.1113 a html:Body ;
    rdf:_1 doc:1.1119 .

doc:1.1119 a html:Form ;
    rdf:_1 doc:1.1150 ;
    rdf:_2 doc:1.1804 ;
    html:action "action_page.php" .

doc:1.1150 a html:Div ;
    rdf:_1 doc:1.1173 ;
    rdf:_10 doc:1.1656 ;
    rdf:_11 doc:1.1660 ;
    rdf:_12 doc:1.1739 ;
    rdf:_2 doc:1.1190 ;
    rdf:_3 doc:1.1243 ;
    rdf:_4 doc:1.1247 ;
    rdf:_5 doc:1.1286 ;
    rdf:_6 doc:1.1371 ;
    rdf:_7 doc:1.1411 ;
    rdf:_8 doc:1.1499 ;
    rdf:_9 doc:1.1553 ;
    html:class "container" .

doc:1.1173 a html:H1 ;
    rdf:_1 doc:1.1173.1 .

doc:1.1173.1 a html:Text ;
    html:fragment "Register" .

doc:1.1190 a html:P ;
    rdf:_1 doc:1.1190.1 .

doc:1.1190.1 a html:Text ;
    html:fragment "Please fill in this form to create an account." .

doc:1.1243 a html:Hr .

doc:1.1247 a html:Label ;
    rdf:_1 doc:1.1266 ;
    html:for "email" .

doc:1.1266 a html:B ;
    rdf:_1 doc:1.1266.1 .

doc:1.1266.1 a html:Text ;
    html:fragment "email" .

doc:1.1286 a html:Input ;
    html:id "email" ;
    html:name "email" ;
    html:placeholder "Enter Email" ;
    html:required "true" ;
    html:type "text" .

doc:1.1371 a html:Label ;
    rdf:_1 doc:1.1388 ;
    html:for "psw" .

doc:1.1388 a html:B ;
    rdf:_1 doc:1.1388.1 .

doc:1.1388.1 a html:Text ;
    html:fragment "Password" .

doc:1.1411 a html:Input ;
    html:id "psw" ;
    html:name "psw" ;
    html:placeholder "Enter Password" ;
    html:required "true" ;
    html:type "password" .

doc:1.1499 a html:Label ;
    rdf:_1 doc:1.1523 ;
    html:for "psw-repeat" .

doc:1.15 a html:Html ;
    rdf:_1 doc:1.21 ;
    rdf:_2 doc:1.1113 .

doc:1.1523 a html:B ;
    rdf:_1 doc:1.1523.1 .

doc:1.1523.1 a html:Text ;
    html:fragment "Repeat Password" .

doc:1.1553 a html:Input ;
    html:id "psw-repeat" ;
    html:name "psw-repeat" ;
    html:placeholder "Repeat Password" ;
    html:required "true" ;
    html:type "password" .

doc:1.1656 a html:Hr .

doc:1.1660 a html:P ;
    rdf:_1 doc:1.1660.1 ;
    rdf:_2 doc:1.1703 ;
    rdf:_3 doc:1.1660.3 .

doc:1.1660.1 a html:Text ;
    html:fragment "" .

doc:1.1660.3 a html:Text ;
    html:fragment "" .

doc:1.1703 a html:A ;
    rdf:_1 doc:1.1703.1 ;
    html:href "#" .

doc:1.1703.1 a html:Text ;
    html:fragment "Terms & Privacy" .

doc:1.1739 a html:Button ;
    rdf:_1 doc:1.1739.1 ;
    html:class "registerbtn" ;
    html:type "submit" .

doc:1.1739.1 a html:Text ;
    html:fragment "Register" .

doc:1.1804 a html:Div ;
    rdf:_1 doc:1.1834 ;
    html:class "container signin" .

doc:1.1834 a html:P ;
    rdf:_1 doc:1.1834.1 ;
    rdf:_2 doc:1.1861 ;
    rdf:_3 doc:1.1834.3 .

doc:1.1834.1 a html:Text ;
    html:fragment "" .

doc:1.1834.3 a html:Text ;
    html:fragment "" .

doc:1.1861 a html:A ;
    rdf:_1 doc:1.1861.1 ;
    html:href "#" .

doc:1.1861.1 a html:Text ;
    html:fragment "Sign in" .

doc:1.21 a html:Head ;
    rdf:_1 doc:1.27 ;
    rdf:_2 doc:1.42 ;
    rdf:_3 doc:1.1058 .

doc:1.27 a html:Title .

doc:1.42 a html:StyleSheet ;
    rdf:_1 doc:1.42.1 .

doc:1.42.1 a html:Text ;
    html:fragment "body {font-family: Arial, Helvetica, sans-serif; background-color: black; } * {box-sizing: border-box;} /* Add padding to containers */.container {padding: 16px; background-color: white;} /* Full-width input fields */ input[type=text], input[type=password] {width: 100%; padding: 15px;  margin: 5px 0 22px 0; display: inline-block; border: none;  background: #f1f1f1;} input[type=text]:focus, input[type=password]:focus {  background-color: #ddd;  outline: none;} /* Overwrite default styles of hr */ hr {   border: 1px solid #f1f1f1;   margin-bottom: 25px;} /* Set a style for the submit button */ .registerbtn {   background-color: #04AA6D;   color: white;   padding: 16px 20px;   margin: 8px 0;   border:  none;  cursor: pointer;   width: 100%;   opacity: 0.9; } .registerbtn:hover {  opacity: 1;} /* Add a blue text color to links */ a {  color: dodgerblue;} /* Set a grey background color and center the text of the \"sign in\" section */ .signin {  background-color: #f1f1f1;  text-align: center;}" .
```

# Tools and dependencies

This repository comes with two, fairly primitive, Python-based tools to handle HTML-documents and RDF-representations of HTML. 

1. HTML2RDF
2. RDF2HTML
3. Playground


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

A. Install all necessary libraries (in this order):

	1. pip install os 
	2. pip install pyshacl
	3. pip install rdflib

NOTE: pyshacl has a dependency with an older RDFlib version. However, for an optimal functioning of the semantic HTML-vocabulary, the most recent release of RDFlib should be used. Hence, it is advised to first install pyshacl and then RDFlib, so that RDFlib is installed having the latest version. This is currently the least instrusive way of handling the dependency, offering accessibility for those not well versed in Python. 

B. Place one or more Turtle-files (*.ttl) in the input folder in htmlvoc\Tools\RDF2HTML\Input. A Turtle-file should represent a HTML-document using the HTML-vocabulary from this repository.

C. Run the script in the command prompt by typing: 

```
python RDF2HTML.py
```

D. Go to the output folder in htmlvoc\Tools\RDF2HTML\Output and grab your HTML-file(s). Additionally included are Turtle-file(s) (*.ttl) that contain the serialized 'html:fragment' properties for the very same HTML-document and the HTML-elements it contains.

## Playground

The tool Playground offers a visual user interface in which a RDF-based representation of an HTML-document can be converted to an actual HTML-document, and an actual HTML-document can be converted to a RDF-based representation of an HTML-document.

![A screenshot of the playground environment](/Examples/Playground.PNG)

### How to use Playground

A. Install all necessary libraries (in this order):

	1. pip install os 
	2. pip install pyshacl
	3. pip install rdflib

B. Run the script in the command prompt by typing: 

```
python playground.py
```

C. Navigate to the URL http://localhost:5000/. Then choose one of two options:

   *Option 1*: Place your RDF-triples representing an HTML-document into the corresponding text area and press the button 'convert to HTML'. The playground will convert the triples to an HTML-document and display this in your browser. This may take some time.

   *Option 2*: Place the HTML-code of your HTML-document into the corresponding text area and press the button 'convert to RDF'. The playground will convert the HTML-document to a RDF-based representation of that document. This should be rather quick.


   Please note: the runtime of RDF2HTML for a rather complex and long HTML-file can be rather large.

## Dependencies 

Both tools make extensive use of [RDFlib](https://rdflib.readthedocs.io/en/stable/index.html). Rdflib is a Python library used for working with Resource Description Framework (RDF) data. RDF is a widely used framework for representing and processing information on the web. It is a standard model for data interchange on the web, particularly for representing metadata and data about resources available on the internet.

Rdflib provides a comprehensive set of tools and utilities for working with RDF data, including parsing and serializing RDF in various formats (such as RDF/XML, Turtle, JSON-LD, and more), querying RDF data using SPARQL, creating RDF graphs, and performing various operations on RDF triples.

The RDF2HTML tool additionally makes use of [PyShacl](https://github.com/RDFLib/pySHACL). PySHACL is a complete open-source implementation of the SHACL W3C specification, with broad use in the community as well. 

# Acknowledgements

We would like to thank Iwan Aucamp @RDFlib for his unrelenting support and accomplishments regarding the open source triple store and related services, as well as Ashley Sommer @PyShacl for his work on the important open source implementation of a SHACL engine. 