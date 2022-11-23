import os, argparse
from config import Config
from app import create_app, db
import app.models

def setup_parser():
    parser = argparse.ArgumentParser(description='Ingest data as a starting point for beanZ', 
                                    epilog="Not all combinations and permutations have been fully tested. Don't be picky")
    parser.add_argument('-v','--verbose', action='store_true', help='increase verbosity')
    parser.add_argument('-d', '--dir', type=str, nargs='+', help='directory from which to read all files (default is ingest_files/)')
    parser.add_argument('-f', '--file', type=str, nargs='+', help='file(s) to ingest')

    return parser

class Ingester():
    def __init__(self, args):
        self.args = args
        self.files = self.collect_filenames()
        self.setUp()
        if self.args.verbose: print(f'[+] Ingester setting up...')

    def setUp(self):
        self.app = create_app(Config)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()
        if self.args.verbose: print(f'[+] Ingester shutting down...')

    def collect_filenames(self):
        path = 'ingest_files/'
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
            text.close()

if __name__ == '__main__':
    
    parser = setup_parser()
    args = parser.parse_args()

    ingester = Ingester(args)

    ingester.ingest_files()
    ingester.tearDown()