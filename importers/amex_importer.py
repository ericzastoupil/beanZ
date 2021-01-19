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

	def identify(self, f):
		if not re.match('Transactions.*\.csv', os.path.basename(f.name)):
			return False

		'''if 'skymiles' in f.name.lower():
			self.account = 'Liabilities:CC:Amex:SkyMiles-Platinum'
		if 'reserve' in f.name.lower():
			self.account = 'Liabilities:CC:Amex:SkyMiles-Reserve'
		else:
			RunTimeError('Please include SkyMiles or Reserve in the filename')
		'''

		return True

	def extractor(self, f):
		entries = []

		with open(f.name) as f:
			for index, row in enumerate(csv.reader(f)):
				trans_date = parse(row[0].split(' ')[0]).date()
				trans_descr = titlecase(row[2])
				trans_amt = row[7]

				if trans_desc == 'Online Payment - Thank You':
					continue

				if trans_desc == 'Payment Received - Thank You':
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
