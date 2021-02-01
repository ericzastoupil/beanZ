from beancount.core.number import D
from beancount.ingest import importer
from beancount.core import account
from beancount.core import amount
from beancount.core import flags
from beancount.core import data
from beancount.core.position import Cost

from dateutil.parser import parse

from titlecase import titlecase

import datetime
import csv
import os
import re

class AmexImporter(importer.ImporterProtocol):

	def __init__(self, currency,
					account_root,
					account_cash,
					account_dividends,
					account_gains,
					account_fees,
					account_external):
		self.currency = currency
		self.account_root = account_root
		self.account_cash = account_cash
		self.account_dividends = account_dividends
		self.account_gains = account_gains
		self.account_fees = account_fees
		self.account_external = account_external

	def name(self):
		'''This method provides a unique ID for each importer instance. It's convenient to
		be able to refer to your importers by a unique name; it gets printed out by the
		identification process, for instance
		'''
		return "AMEX Credit Card Importer"

	def identify(self, f):
		'''This method just returns TRUE if this importer can handle the given file. This
		method must be implemented, amnd all the tools invoke it to figure out the list of
		(file, importer) pairs.
		'''

		if not re.match('AMEX.*\.csv', os.path.basename(f.name)):
			return False

		print("Running "+self.name()+" on "+os.path.basename)

		return True

	def extract(self, f):
		'''This is called to attempt to extract some Beancount directives from the file 
		contents. It must create the directives by instantiating the objects defined in
		beancount.core.data and return them.
		'''

		entries = []

		with open(f.name) as f:
			for index, row in enumerate(csv.reader(f)):
				#index is row number
				#row is a list of values in that row
				trans_date = parse(row[0].split(' ')[0]).date()
				trans_descr = titlecase(row[1])
				trans_amt = row[4]

				if trans_desc == 'AUTOPAY PAYMENT - THANK YOU':
					continue

				meta = data.new_metadata(f.name, index)
	
				txn = data.Transaction(
					meta = meta,
					date = trans_date,
					flags = flags.FLAG_OKAY,
					payee = trans_desc,
					narration = "",
					tags = set(),
					links = set(),
					postings = [],
				)

				txn.postings.append(
					data.Posting(
						self.account,
						amount.Amount(-1*D(trans_amt), 'USD'),
						None, None, None, None
					)
				)

				entries.append(txn)

		return entries

	def file_account(self, f):
		'''This method returns the root account associated with this importer. 
		This is where the downloaded file will be moved by the filing script.
		'''
		
		return False

	def file_date(self, f):
		'''If a date cane be extracted from the statement's contents, return
		it here. This is useful for dated PDF statements... it's often possible
		using regular expresions to grep out the date from a PDF converted to
		text. This allows the filing script to prepend a relevant date instead
		of using the date when the file was downloaded (the default).
		'''

		return None
		
	def file_name(self, f):
		'''It's most convenient not to bother renaming downloaded files. Oftentimes,
		the files generated from your bank either all have a unique name and they
		end up getting renamed by your browser when you download multiple ones and
		the names collide. This function is used for the importer to provide a "nice"
		name to file the document under.
		'''

		return False
