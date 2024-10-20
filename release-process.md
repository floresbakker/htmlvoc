# Release process

New versions of the HTML Vocabulary are released on GitHub.

For each released version of the HTML Vocabulary, we offer a special download for use in the external tools rdflib and pyShacl. This special download works around the following known limitations and known bugs in these external tools:

- No support for named graphs. Fix: change the TriG file into a Turtle file.
- No support for the default value of `group_concat()`, i.e. the space character. Fix: set the default value explicitly.
- Low performance in RDFlib based scripts for datatype IRIs that are `rdf:HTML`. Workaround if performance is too low: change `rdf:HTML` to `xsd:string` in the SHACL rule for html fragment serialisation. Issue is caused by erroneous behavior of the html5lib package that is used by RDFlib.
