#**Md2Tex**
----------

**Markdown** allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML).

**LaTeX** is a document preparation system and document markup language.

Markdown is exponentially easier to learn than LaTeX because of its simplicity. Basics of Markdown can be learnt within minutes. LaTeX is vast and complex. However, basics of complex LaTeX programming can be toned down and substituted with Markdown codes. With ***Md2Tex*** all the basics of Markdown can be converted to standard LaTeX. Auto inclusion of LaTeX packages.

---
#Getting Started
Learn [Basic Markdown](http://daringfireball.net/projects/markdown/syntax#link). To cover the limitations of Markdown use tilde(~) in order to specify effects.

    ~ effext : text ~

Examples:

* ~ title : Yea the Title ~
* ~ author : My Name ~
* ~ blue : This text goes my favorite color. ~
* ~ import code : imports_code.py ~


Seethe list of effects in data.py. LaTeX code works fine while writing Markdown codes too so writing Tex syntax in the md file is possible.

----

#How to Run
Clone this shit to ur computer. Write ur stuffs in a_file.md. Then step in the following codes.

    $ python md2tex a_file.md a_file.tex article

------
