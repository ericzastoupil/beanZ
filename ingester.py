import os, argparse
import datetime
from config import Config
from app import create_app, db
from app.models import Transaction, Account, Merchant

def setup_parser():
    parser = argparse.ArgumentParser(prog='Ingester',
                                    description='Ingest data as a starting point for beanZ', 
                                    epilog="Not all combinations and permutations have been fully tested. Don't be picky.")
    parser.add_argument('-v','--verbose', action='store_true', help='increase verbosity')
    parser.add_argument('-d', '--dir', type=str, nargs='+', help='directory from which to read all files (default is ingest_files/)')
    parser.add_argument('-f', '--file', type=str, nargs='+', help='file(s) to ingest')
    parser.add_argument('-x', '--clear', action='store_true', help='clears all stored transactions')
    parser.add_argument('-t', '--trans', action='store_true', help='add a single user')
    parser.add_argument('-u', '--user', type=str, nargs='+', help='add a single user')
    parser.add_argument('-a', '--account', type=str, nargs='+', help='add a single account')
    parser.add_argument('-m', '--merchant', type=str, nargs='+', help='add a single merchant')

    return parser

class Ingester():
    def __init__(self, args):
        self.args = args
        self.path = 'ingest_files/'
        self.files = self.collect_filenames()
        self.setUp()
        if self.args.verbose: print(f'[+] Ingester setting up...')

    def __del__(self):
        if self.args.verbose: print(f'[+] Ingester shutting down...')

    def setUp(self):
        self.app = create_app(Config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def clear_transactions(self):
        if self.args.verbose: print(f'[!] Clearing all transactions...')
    
        db.session.query(Transaction).delete()
        db.session.commit()

    def single_trans(self):
        user_id=1
        amount=1.23
        date_trans=['12/31/2021', '%m/%d/%Y']
        account_id=1
        merchant_id=1
        
        if self.args.verbose: 
            print(f'[+] Adding single transaction...')
            print(f'    user_id: {user_id}')
            print(f'    amount: {amount}')
            print(f'    date_trans: {date_trans[0]}')
            print(f'    account_id: {account_id}')
            print(f'    merchant_id: {merchant_id}')

        t = Transaction(user_id=user_id,
                    amount=amount,
                    date_transaction=datetime.datetime.strptime(date_trans[0], date_trans[1]), 
                    account_id=account_id,
                    merchant_id=merchant_id)
        
        db.session.add(t)
        db.session.commit()

    def single_account(self):
        account_owner=1
        type_id=1
        institution_id=1
        account_name=self.args.account[0] #maybe Institution + Type? ie Chase Checking
        desc=''
        
        if self.args.verbose: 
            print(f'[+] Adding single account...')
            print(f'    account_owner: {account_owner}')
            print(f'    type_id: {type_id}')
            print(f'    institution_id: {institution_id}')
            print(f'    account_name: {account_name}')
            print(f'    desc: {desc}')

        a = Account(account_owner=account_owner,
                    type_id=type_id,
                    institution_id=institution_id, 
                    account_name=account_name,
                    desc=desc)
        
        db.session.add(a)
        db.session.commit()

    def single_merchant(self):
        merchant_name=self.args.merchant[0]
        desc=self.args.merchant[1]
        
        if self.args.verbose: 
            print(f'[+] Adding single merchant...')
            print(f'    merchant_name: {merchant_name}')
            print(f'    desc: {desc}')

        m = Merchant(merchant_name=merchant_name,
                    desc=desc)
        
        db.session.add(m)
        db.session.commit()

    def collect_filenames(self):
        path = self.path
        files = []

        #if no specific directories or files given, take files from default directory
        #else take from command line
        if not self.args.dir and not self.args.file:
            for f in os.listdir(path):
                files.append(os.path.join(path,f))
        else: 
            if self.args.dir:
                for dir in self.args.dir:
                    for f in os.listdir(dir):
                        files.append(os.path.join(dir,f))
            if self.args.file:
                for file in self.args.file:
                    files.append(file)

        if self.args.verbose: print(f'[+] Files to ingest: {files}')

        return files

    def ingest_files(self):
        for file in self.files:
            if args.verbose: print(f'[+] Ingesting file: {file}')
            text = open(file, 'r')
            lines = text.readlines()
            count = 0
            for line in lines:
                count += 1
                if args.verbose: print(f"File {file}: Line {count}: {line.strip()}")
                self.record(line)
            text.close()

    def record(self, line):
        trans = line.split(',')
        t = Transaction(user_id=1, 
                        amount=float(trans[6]),
                        date_transaction=datetime.datetime.strptime(trans[2], '%m/%d/%Y'), 
                        account_id=7,
                        merchant_id=7)
        db.session.add(t)
        db.session.commit()

if __name__ == '__main__':
    
    parser = setup_parser()
    args = parser.parse_args()

    ingester = Ingester(args)

    if args.clear:
        ingester.clear_transactions()
    elif args.trans:
        ingester.single_trans()
    else:
        ingester.ingest_files()
    
    ingester.tearDown()