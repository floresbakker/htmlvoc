# Release process

New versions of the HTML Vocabulary are released on GitHub.

For each released version of the HTML Vocabulary, we offer a special download for use in the external tools rdflib and pyShacl. This special download works around the following known limitations and known bugs in these external tools:

- No support for named graphs. Fix: change the TriG file into a Turtle file.
- No support for the default value of `group_concat()`, i.e. the space character. Fix: set the default value explicitly.
- No support for datatype IRIs that are not `xsd:string`. Fix: change `rdf:HTML` to `xsd:string`.
- Nested `filter not exists` are not supported. Fix: use `minus`.
