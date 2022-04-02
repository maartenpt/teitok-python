import lxml.etree as etree
import flair
from flair.data import Sentence
import sys

filenames = {}

def readxml(xmlfile = ""):
	if xmlfile == "":
		if len(sys.argv) == 1:
			print("Please provide an TEITOK/XML filename")
			exit()
		xmlfile = sys.argv[1]
	xmlf = etree.parse(xmlfile)
	filenames[xmlf] = xmlfile
	return xmlf

def save(xmlf, filename=""):
	if filename == "":
		filename = filenames[xmlf]
	print("output written to " + filename)
	xmlf.write(filename,encoding="UTF-8")	

def readsent(xmlf, **opts):
	sentence = {}
	tokens = []
	selm = "s"	
	if 'selm' in opts.keys():
		selm = opts['selm']
	if 'sentid' in opts.keys():
		sentid = opts['sentid']
		sentence['id'] = sentid
		tokxp = "//" + selm + "[@id=\""+sentid+"\"]//tok"
	else:
		tokxp = "//tok"

	tokcnt = 0
	text = ""
	for tok in xmlf.findall(tokxp):
		newtok = {}
		if "form" in tok.keys():
			word = tok.attrib["form"]
		else:
			word = tok.text
		text = text + word + " "
		newtok['word'] = word
		for attr in tok.items():
			key = attr[0]
			val = attr[1]
			newtok[key] = val
		tokens.append(newtok)
		tokcnt = tokcnt + 1
	
	sentence['text'] = text
	sentence['tokens'] = tokens
	return sentence

def printconllu(sentence):
	flds = "ord,word,lemma,upos,xpos,feats,ohead,deprel,deps,misc".split(",")
	print("# sent_id = " + sentence['id'])
	print("# text = " + sentence['text'])
	ord = 1
	for token in sentence['tokens']:
		vals = {}
		tokid = token['id']
		miscs = ["tokId="+tokid]
		if "ner" in token.keys():
			miscs.append(token['ner'])
		for fld in flds:
			if fld in token.keys():
				val = token[fld]
				if val == "":
					val = "_"
				vals[fld] = val
			else:
				vals[fld] = "_"
		misc = "|".join(miscs)
		print(ord,vals['word'],vals['lemma'],vals['upos'],vals['xpos'],vals['feats'],vals['ohead'],vals['deprel'],vals['deps'],misc,sep="\t")
		ord = ord+1
	print("")

def readsents(xmlf, **opts):
	sentences = []
	selm = "s"	
	if 'selm' in opts.keys():
		selm = opts['selm']
	sxp = "//" + selm	
	xsent = xmlf.findall(sxp)
	if xsent:
		for sent in xsent:
			sentid = sent.attrib['id']
			sentence = readsent(xmlf, selm=selm, sentid=sentid )
			sentences.append(sentence)
	else:
		sentid = "null"
		sentence = readsent(xmlf)
		sentences.append(sentence)
	return sentences
	
def insertbefore(node, newchild):
	idx = node.getparent().index(node)
	node.getparent().insert(idx,newchild)
