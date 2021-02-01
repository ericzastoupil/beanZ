import os, sys

#beancount doesn't run from this directory
sys.path.append(os.path.dirname(__file__))

#importers located in the importers directory
from importers import amex, usaa

CONFIG = [
	amex.AmexImporter(),
	usaa.USAAImporter()
]
