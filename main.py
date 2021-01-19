import os
import easygui
import beancount
import importers.amex_importer
import importers.usaa_importer

if __name__ == '__main__':
	print("Hello World")

	'''if os.environ.get('DISPLAY','')=='':
		print('no display found, using :0.0')
		os.environ.__setitem__('DISPLAY',':0.0')
	easygui.ynbox('Stuff or things?', 'Title', ('Stuff', 'Things'))
	'''
