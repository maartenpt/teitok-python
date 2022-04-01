import lxml.etree as etree
import flair
from flair.data import Sentence

def readsent(xmlf, sentid=""):
	sentence = Sentence() 
	if sentid:
		sentence.add_label("sentid", sentid )
		tokxp = "//s[@id=\""+sentid+"\"]//tok"
	else:
		tokxp = "//tok"

	tokcnt = 0
	for tok in xmlf.findall(tokxp):
		if "form" in tok.keys():
			form = tok.attrib["form"]
		else:
			form = tok.text
		sentence.add_token(form)
		for attr in tok.items():
			sentence[tokcnt].add_tag(attr[0], attr[1])
		tokcnt = tokcnt + 1

	return sentence

def readsents(xmlf):
	sentences = {}
	for sent in xmlf.findall("//s"):
		sentid = sent.attrib['id']
		sentence = readsent(xmlf, sentid)
		sentences[sentid] = sentence
	return sentences

def toconllu(sentence):
	sentid = "|".join(x.value for x in sentence.get_labels('sentid'))
	flds = "ord,form,lemma,upos,xpos,feats,ohead,deprel,deps,misc".split(",")
	print("# sent_id = " + sentid)
	print("# text = " + sentence.to_plain_string())
	ord = 1
	for token in sentence:
		d = {}
		tokid = token.get_tag('id').value
		form = token.text
		miscs = ["tokId="+tokid]
		if token.get_tag('ner') and token.get_tag('ner').value != "":
			miscs.append(token.get_tag('ner').value)
		for fld in flds:
			val = token.get_tag(fld).value
			if val == "":
				val = "_"
			d[fld] = val
		misc = "|".join(miscs)
		print(ord,form,d['lemma'],d['upos'],d['xpos'],d['feats'],d['ohead'],d['deprel'],d['deps'],misc,sep="\t")
		ord = ord+1
	print("")

def writeback(xmlf, sentences, attrs = ""):
	toklist = {}
	doatts = attrs.split(",")
	for tok in xmlf.findall("//tok"):
		tokid = tok.attrib['id']
		toklist[tokid] = tok
	for sentid in sentences:
		sentence = sentences[sentid]
		for token in sentence:
			tokid = token.get_tag('id').value
			xtok = toklist[tokid]
			for attr in doatts:
				val = token.get_tag(attr).value
				if val != "" and val != "_":
					xtok.attrib[attr] = val
	
