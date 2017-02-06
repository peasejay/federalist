#!/usr/bin/env/python
import re


alltext = ''
sections = []
with open('pg1404.txt') as fp:
    for line in fp:
        alltext += line

#print alltext

def small_cap_replace(match):
    if match.start(1) == 0:
        thestring = match.group(1).lower()
        replacement = "\\textsc{" + thestring[0].upper() + thestring[1:] + "}"
    else:
        replacement = "\\textsc{" + match.group(1).lower() + "}"
    return replacement

sections = alltext.split("\n\n\n\n\n")

new_sections = []

for section in sections:
    temp_section = []
    paragraphs = section.split("\n\n")

    for paragraph in paragraphs:
        temp_section.append(paragraph.replace("\n", " "))

    new_sections.append(temp_section)


files = []

for section_index, section in enumerate(new_sections):
    if section_index < 3:
        continue
    if section_index > 87:
        continue

    article_number = section_index - 2
    filename = "federalist_%02d.tex" % (article_number) 
    files.append(filename)
    # preprocess paragraphs to find footnotes
    with open(filename, 'w') as fp:
        #fp.write("\\documentclass[10pt]{book}\n")

        #fp.write("\\newcommand\Chapter[2]{\chapter[#1: {\itshape#2}]{#1\\[2ex]\Large\itshape#2}}")
        #fp.write("\\begin{document}\n")
        footnotes = {}
        for paragraph_index, paragraph in enumerate(section):
            matches = re.match(r"^(\d+)\. (.*)", paragraph)
            if matches:
                footnotes[matches.group(1)] = matches.group(2)

        for paragraph_index, paragraph in enumerate(section):
            if paragraph_index == 0:
                pass
                #fp.write("\\section[%s: %s]{%s\\\\ {\\large %s}}\n" % (paragraph, section[1], paragraph, section[1]))
                fp.write("\\chapter[%s: %s]{%s\\\\ {\\small %s}}\n" % (paragraph.replace("FEDERALIST ", ""), section[1], paragraph.replace("FEDERALIST ", ""), section[1]))
            elif paragraph_index == 1:
                pass
                #fp.write("\\section{%s}\n" % (paragraph))
            elif paragraph_index == 2:
                pass
                #fp.write("<h5>%s</h5>\n" % (paragraph))
            elif paragraph_index == 3:
                pass
                #fp.write("<h6>%s</h6>\n" % (paragraph))
            else:
                # replace contents with footnotes
                for key, value in footnotes.iteritems():
                    paragraph = paragraph.replace("(%d)" % (int(key)), "\\footnote{%s}" % (value))

                the_last = False
                if paragraph == "PUBLIUS":
                    the_last = True

                # replace capitalized text with smallcaps
                p = re.compile('([A-Z][A-Z ]{3,})')
                paragraph = p.sub(small_cap_replace, paragraph)

                # fix quotes, maybe
                p = re.compile('(")(.*?)(")')
                paragraph = p.sub(r"``\2\3", paragraph)

                matches = re.match(r"^(\d+)\. (.*)", paragraph)
                if matches:
                    continue
                
                if paragraph_index == 4:
                    fp.write("%s\n\\vspace{.25cm}\n\n" % (paragraph))
                elif the_last:
                    fp.write("\\vspace{.5cm}\n%s\n" % (paragraph))
                else:
                    fp.write("%s\n\n" % (paragraph))

        #fp.write("\\end{document}\n")

with open('federalist_main.tex', 'w') as fp:
    fp.write("\\documentclass[10pt]{book}\n")
    fp.write("\\usepackage[utf8]{inputenc}\n")
    fp.write("\\title{The Federalist Papers}\n")
    fp.write("\\author{Alexander Hamilton, James Madison and John Jay}\n")
    fp.write("\\renewcommand{\\chaptername}{}\n")
    fp.write("\\renewcommand{\\thechapter}{}\n")
    
    #fp.write("\\newcommand\Chapter[2]{\chapter[#1: {\itshape#2}]{#1\\[2ex]\Large\itshape#2}}")
    fp.write("\\begin{document}\n")
    fp.write("\\maketitle\n")
    fp.write("\\tableofcontents\n")
    fp.write("\\newpage\n")
    for this_file in files:
        fp.write("\\include{%s}\n" % (this_file.replace(".tex","")))
    fp.write("\\end{document}\n")