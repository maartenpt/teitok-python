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
