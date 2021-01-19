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

class USAAImporter(importer.ImporterProtocol):

	def __init__(self, currency, account_root, account_cash, account_dividends, account_gains, account_fees, account_external):
		self.currency = currency
		self.account_root = account_root
		self.account_cash = account_cash
		self.account_dividends = account_dividends
		self.account_gains = account_gains
		self.account_fees = account_fees
		self.account_external = account_external

	def identify(self, f):
		return (re.match("stuffandthings.csv", path.basename(f.name)) and
				re.match("DATE,TYPE,REF", f.head()))

	def file_account(self, f):
		return "things"

	def file_date(self, f):
		return "things"

	def file_name(self, f):
		return "things"

	def extract(self, f):
		entries = []

		with open(f.name) as f:
			for index, row in enumerate(csv.reader(f)):
				trans_date = parse(row[2].split('/')[0]).date()
				trans_descr = titlecase(row[4])
				trans_amt = row[6]

				if 'AMEX EPAYMENT' in trans_desc:
					continue
				if 'USAA FUNDS TRANSFER' in trans_desc:
					continue
				if 'ALLY BANK' in trans_desc:
					continue
				if 'USAA CREDIT CARD PAYMENT' in trans_desc:
					continue
				if 'AMZ_STORECRD_PMT' in trans_desc:
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
						amount.Amount(-1*D(trans_amt), self.currency),
						None, None, None, None
					)
				)

				entries.append(txn)

		return entries
