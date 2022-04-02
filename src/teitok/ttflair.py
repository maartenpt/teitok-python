import lxml.etree as etree
import flair
from flair.data import Sentence

def obj2sent(obj):
	sentence = Sentence() 
	tokcnt = 0
	for tok in obj['tokens']:
		for attr in tok.keys():
			val = tok[attr]
			if attr == "word":
				sentence.add_token(val)
			else:
				sentence[tokcnt].add_tag(attr, val)
		tokcnt = tokcnt + 1
	return sentence


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
	
