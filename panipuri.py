#!usr/bin/python

#Panipuri Converter

import sys,os

if(sys.argv[1][-2:]!='md'):
	print 'Error md'
	exit()


FALSE=0
TRUE=1
OFF=0
ON=1


title_status=OFF
content_status=OFF
section_number=0
table_status=OFF
table_head=OFF
unordered_list=[]
unordered_list.append(OFF)
list_tab=0
linenumber=0



md = open(sys.argv[1],'r')
tex = open('latex.tex','w+')
tex_body = open('latexbody.tex','w+')

tex.write('\documentclass[12pt]{article}\n\n')
tex.write('%packages\n')

tex_body.write('\n\n\\begin{document}\n\n\n\n\n')


def structure(sentence):
	
	global content_status,title_status,section_number

	if(sentence[1]!='#'):
		if(content_status==OFF and title_status==OFF):
			title_status=content_status=title(sentence[1:][:-1])
		else:
			if(title_status==ON):
				print 'Title already used'
			if(content_status==ON):
				print 'Content before title'
	elif(sentence[2]!='#'):
		content_status=section_title(sentence[2:][:-1])			
		section_number=1
	elif(sentence[3]!='#'):
		if(section_number>0):
			content_status=sub_section_title(sentence[3:][:-1])
		else:
			print linenumber
			print 'Subsection before section'
		section_number=2
	elif(sentence[4]!='#'):
		if(section_number>1):
			content_status=subsub_section_title(sentence[4:][:-1])
		else:
			print linenumber
			print 'Subsubsection before subsection'





def title(name):

	tex_body.write('\\title{'+name+'}\n\maketitle\n\n\n')
	return TRUE



def section_title(name):

	tex_body.write('\section{'+name+'}\n')
	return ON 

def sub_section_title(name):

	tex_body.write('\subsection{'+name+'}\n')
	return ON 

def subsub_section_title(name):

	tex_body.write('\subsubsection{'+name+'}\n')
	return ON 


def section_content(sentence):

	
	while(sentence.find('**')!=-1):
		sentence=sentence.replace('**',' \\textbf{',1)
		sentence=sentence.replace('**','}',1)

	while(sentence.find('*')!=-1):
		sentence=sentence.replace('*',' \\textit{',1)
		sentence=sentence.replace('*','}',1)

	while(sentence.find('![Alt text](')!=-1):
		add_package('graphicx')
		sentence=sentence.replace('![Alt text](',' \\includegraphics{',1)
		sentence=sentence.replace(')','}',1)

	while(sentence.find('](')!=-1):
		add_package('hyperref')
		label=sentence[sentence.find('[')+1:sentence.find(']')]
		link=sentence[sentence.find('(')+1:sentence.find(')')]
		sentence=sentence.replace(sentence[sentence.find('['):sentence.find(')')+1],'\href{'+link+'}{'+label+'}',1)


	tex_body.write(sentence)
	
	return ON


def table_effect(sentence):

	global nextsentence
	sentence=sentence.replace('|','&')

	nextsentence=nextsentence[:-1]+'|\n'
	if(table_status==OFF):

		print nextsentence
		tex_body.write('\\begin{tabular}{')

		for i in range(0,column):
		
			alignment='l'
			counter=nextsentence.find('|')
			print counter
			if(nextsentence[counter-1]==':'):
				alignment='r'
				if(nextsentence[0]==':'):
					alignment='c'
			tex_body.write('|'+alignment)
			nextsentence=nextsentence[(counter+1):]
			print alignment

		tex_body.write('|}\n\hline\n')

	tex_body.write(sentence[:-1]+'\\\\\n')
	
	if(table_status==OFF):
		tex_body.write('\\hline\n')

	return ON


def row_slicer(sentence):

	if(sentence[:1]=='|'):
		sentence=sentence[1:]
	if(sentence[:-1]=='|'):
		sentence=sentence[-1:]

	return sentence



def sentence_list(sentence):
	if(unordered_list[list_tab]==OFF):
		tex_body.write('\\begin{itemize}\n')
	tex_body.write('\item ' + sentence[2:])
		
	return ON
	

def add_package(package):

	tex.seek(0)
	package_virgin=TRUE
	package='\usepackage{'+package+'}\n'

	for line in tex.readlines():
		if(line==package):
			package_virgin=FALSE
	
	if(package_virgin):
		tex.write(package)




	

#main

mdfile=md.readlines()+['\n\n']
md.seek(0)



for line in md.readlines()+['\n\n']:


	sentence=line
	linenumber+=1
	line_effect_virgin=TRUE


	
	if(sentence[0]=='#'):
		
		structure(sentence)
		line_effect_virgin=FALSE


	#


	if(sentence.count('|') and line_effect_virgin):
		
		sentence=row_slicer(sentence)
		nextsentence=row_slicer(mdfile[linenumber])

		
		if(table_head==ON):
			table_status=table_effect(sentence)

		if(sentence.count('|')==nextsentence.count('|') and nextsentence.count('-')):
			column=nextsentence.count('|')+1
			table_status=table_effect(sentence)
		else:
			table_head=ON
		
		
		line_effect_virgin=FALSE

	elif(table_status==ON):

		tex_body.write('\hline\n\end{tabular}\n')
		table_status=OFF
		table_head=OFF


	#

	
	if( sentence[:list_tab]=='\t'*list_tab and (sentence[list_tab]=='*' or sentence[list_tab]=='+' or sentence[list_tab]=='-')  and sentence[list_tab*2+1]==' '):
		unordered_list[list_tab]=sentence_list(sentence)
		line_effect_virgin=FALSE
	
	elif( sentence[:(list_tab+1)]=='\t'*(list_tab+1) and (sentence[list_tab+1]=='*' or sentence[list_tab+1]=='+' or sentence[list_tab+1]=='-')  and sentence[list_tab+2]==' '):
		list_tab+=1
		unordered_list.append(OFF)
		unordered_list[list_tab]=sentence_list(sentence)
		line_effect_virgin=FALSE
	

	elif(unordered_list[list_tab]==ON):
		print 'qwe'
		if(list_tab!=OFF):
			print list_tab
			list_tab-=1
			unordered_list.pop()
			print unordered_list[list_tab]
		tex_body.write('\end{itemize}\n')
		unordered_list[list_tab]=OFF


	#

	
	if(line=='\n'):
		tex_body.write('\\\\\n')
		
	if(line_effect_virgin):
		content_status=section_content(sentence)




	









tex_body.write('\n\n\end{document}\n')

tex_body.seek(0)
for line in tex_body.readlines():
	tex.write(line)


md.close()
tex.close()
tex_body.close()
os.system('rm latexbody.tex')




print 'done'


######END#########
