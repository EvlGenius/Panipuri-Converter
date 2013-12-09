#!usr/bin/python

#Panipuri Converter

import sys,os
from Tkinter import *

if(sys.argv[1][-2:]!='md'):
	print 'Error md'
	exit()

doc_class=sys.argv[2].lower()

FALSE=0
TRUE=1
OFF=0
ON=1


title_status=OFF
section_number=0
table_status=OFF
table_head=OFF
unordered_list=[]
unordered_list.append(OFF)
list_tab=0
linenumber=0



color=['apricot','bittersweet','blue']

effect_name_1=['italic','emphasis','box']
effect_code_1=['\\textit','\emph','\\fbox']

effect_name_2=['huge','large','abstract','equation']


md = open(sys.argv[1],'r')
tex = open('latex.tex','w+')
tex_body = open('latexbody.tex','w+')

tex.write('\documentclass[12pt]{'+doc_class+'}\n\n')
tex.write('%packages\n')

tex_body.write('\n\n\\begin{document}\n\n\n\n\n')


def structure(sentence):
	
	global content_status,title_status,section_number

	

	if(sentence[1]!='#'):
		if(doc_class=='letter'):
			print 'Error'
		else:
			tex_body.write('\part{'+sentence[1:][:-1]+'}\n')
	elif(sentence[2]!='#'):		
		tex_body.write('\chapter{'+sentence[2:][:-1]+'}\n')
	elif(sentence[3]!='#'):		
		if(doc_class=='letter'):
			print 'Error'
		else:
			tex_body.write('\section{'+sentence[3:][:-1]+'}\n')
	elif(sentence[4]!='#'):		
		if(doc_class=='letter'):
			print 'Error'
		else:
			tex_body.write('\subsection{'+sentence[4:][:-1]+'}\n')
	elif(sentence[5]!='#'):		
		if(doc_class=='letter'):
			print 'Error'
		else:
			tex_body.write('\subsubsection{'+sentence[5:][:-1]+'}\n')
	elif(sentence[6]!='#'):		
		if(doc_class=='letter'):
			print 'Error'
		else:
			tex_body.write('\paragraph{'+sentence[6:][:-1]+'}\n')
	elif(sentence[7]!='#'):		
		if(doc_class=='letter'):
			print 'Error'
		else:
			tex_body.write('\subparagraph{'+sentence[7:][:-1]+'}\n')







def section_content(sentence):

	sentence=md_effect(sentence,'**','\\textbf{','}')
	sentence=md_effect(sentence,'*','\\textit{','}')
	sentence=md_effect(sentence,'<<','\\begin{flushleft}','\end{flusfleft}')
	sentence=md_effect(sentence,'>>','\\begin{flushright}','\end{flusfright}')
	sentence=md_effect(sentence,'==','\\begin{center}','\end{center}')


	while(sentence.find('![Alt text](')!=-1):
		add_package('','graphicx')
		sentence=sentence.replace('![Alt text](',' \\includegraphics{',1)
		sentence=sentence.replace(')','}',1)

	while(sentence.find('](')!=-1):
		add_package('','hyperref')
		label=sentence[sentence.find('[')+1:sentence.find(']')]
		link=sentence[sentence.find('(')+1:sentence.find(')')]
		sentence=sentence.replace(sentence[sentence.find('['):sentence.find(')')+1],'\href{'+link+'}{'+label+'}',1)
	
	while(sentence.find('~')!=-1):
		
		effect=sentence[sentence.find('~')+1:sentence.find(':')]
		print effect
		effect=slicer(effect,' ')
		text=sentence[sentence.find(':')+1:sentence[(sentence.find('~')+1):].find('~')+1]
		print text
	
			
		if(effect=='title'):
			if(bluntfile.find('~author')==-1):
				sentence=tilde_effect(sentence,'','','\\title{',text+'}\maketitle')
			else:
				sentence=tilde_effect(sentence,'','','\\title{',text+'}')
		
		elif(effect=='author'):
			sentence=tilde_effect(sentence,'','','\\author{',text+'}\maketitle')
			
		
		elif(effect=='footnote'):
			sentence=tilde_effect(sentence,'','','\\footnote{',text+'}')
		
		elif(effect=='marginnote'):
			sentence=tilde_effect(sentence,'','marginnote','\marginnote{',text+'}')

		elif(effect in color):
			sentence=tilde_effect(sentence,'usenames,dvipsnames','color','\color{'+effect+'}{',text+'}')
		
		elif(effect in effect_name_1):
			sentence=tilde_effect(sentence,'','',effect_code_1[effect_name_1.index(effect)]+'{',text+'}')

		elif(effect in effect_name_2):
			sentence=tilde_effect(sentence,'','','\\begin{'+effect+'}',text+'\end{'+effect+'}')

		elif(effect=='fraction'):
			index=text.find('/')
			if(index==-1):
				print 'error'
			else:
				sentence=tilde_effect(sentence,'','','$\\frac{',text[:index]+'}{'+text[index+1:]+'}$')

		elif(effect=='square root' or effect=='sqrt'):
			sentence=tilde_effect(sentence,'','','$$\\sqrt{',text+'}$$')
			


		elif(effect[:1]=='#' and len(effect)==7):
			
			effect=effect[1:]
			efflen=len(effect)
			#print efflen
			effect=tuple(int(effect[i:i+efflen/3],16) for i in range(0,efflen,efflen/3))
			effect=[float(x) for x in effect]
			effect=[x/255 for x in effect]
			effect=','.join(str(x) for x in effect)

			sentence=tilde_effect(sentence,'usenames,dvipsnames','color','{\color[rgb]{'+effect+'}{',text+'}')
		
		elif(effect.find(',')==2):
			add_package('usenames,dvipsnames','color')
			print effect
			effect=[int(s) for s in effect.split() if s.isdigit()]
			print effect
			if(all(isinstance(item,int) for item in effect)):
				print 'asdasd'
				effect=[x/255 for x in effect]
			print effect
			effect=','.join(str(x) for x in effect)
			print effect
			sentence=sentence.replace(sentence[sentence.find('~'):sentence.find(':')],'{\color[rgb]{'+effect+'}{',1)
			sentence=sentence.replace(sentence[sentence.find(':'):sentence.find('~')+1],text+'}',1)
		else:
			break



	tex_body.write(sentence)
	
	return ON


def md_effect(sentence,sign,begin,end):

	while(sentence.find(sign)!=-1):
		sentence=sentence.replace(sign,begin,1)
		sentence=sentence.replace(sign,end,1)

	return sentence


def tilde_effect(sentence,option,package,effect,text):

	if(package!=''):
		add_package(option,package)
		
	sentence=sentence.replace(sentence[sentence.find('~'):sentence.find(':')],effect,1)
	sentence=sentence.replace(sentence[sentence.find(':'):sentence.find('~')+1],text,1)

	return sentence


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


def slicer(sentence,character):

	left2trim=TRUE
	right2trim=FALSE

	while(left2trim and right2trim):
		if(sentence[:1]==character):
			sentence=sentence[1:]
		else:
			left2trim=TRUE
		if(sentence[:-1]==character):
			sentence=sentence[-1:]
		else:
			right2trim=FALSE

	return sentence



def sentence_list(sentence):
	if(unordered_list[list_tab]==OFF):
		tex_body.write('\\begin{itemize}\n')
	tex_body.write('\item ' + sentence[(2+list_tab):])
		
	return ON
	

def add_package(option,package):

	tex.seek(0)
	package_virgin=TRUE
	package='\usepackage['+option+']{'+package+'}\n'

	for line in tex.readlines():
		if(line==package):
			package_virgin=FALSE
	
	if(package_virgin):
		tex.write(package)




	

#main

bluntfile=md.read()
md.seek(0)
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
		
		sentence=slicer(sentence,'|')
		nextsentence=slicer(mdfile[linenumber],'|')

		
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
	print list_tab
	print unordered_list[list_tab]
	print sentence
	
	if( sentence[:list_tab]=='\t'*list_tab and (sentence[list_tab]=='*' or sentence[list_tab]=='+' or sentence[list_tab]=='-')  and sentence[list_tab+1]==' '):
		print 'a'
		unordered_list[list_tab]=sentence_list(sentence)
		line_effect_virgin=FALSE
	
	elif( sentence[:(list_tab+1)]=='\t'*(list_tab+1) and (sentence[list_tab+1]=='*' or sentence[list_tab+1]=='+' or sentence[list_tab+1]=='-')  and sentence[list_tab+2]==' '):
		print 'b'
		list_tab+=1
		unordered_list.append(OFF)
		unordered_list[list_tab]=sentence_list(sentence)
		line_effect_virgin=FALSE
	

	elif(unordered_list[list_tab]==ON):
		print 'c'
		unordered_list[list_tab]=OFF
		if(list_tab!=OFF):
			print 'd'
			list_tab-=1
			#unordered_list.pop()
		tex_body.write('\end{itemize}\n')


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
