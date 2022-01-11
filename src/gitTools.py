import subprocess
import traceback
from typing import List
import requests
import re
from src import tables, crud
from src.types import FirstHash, SimpleGitObject, GitObjectType
import os

class Git:
    def __init__(self, proxies : dict = None, timeout: int = 5):
        self.session = requests.session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.3538.77 Safari/537.36'
        self.session.proxies = proxies
        self.session.timeout = timeout
        try:
            os.chdir('gitFiles/.git')
        except:
            pass

    def detectGitFile(self, site_url : str) -> bool:
        try:
            check_url = self.reformat_url(site_url) + '.git/HEAD'
            request = self.session.get(check_url)
            if not request.ok:
                return False

            request.encoding = 'utf-8'

            return request.text.startswith('ref: refs/')

        except:
            return False

    def getFirstHashes(self, site_url: str) -> List[FirstHash]:
        try:
            find = False
            text = str()
            groups = None
            re_search = r'(?P<first_hash>\w{40}) (?P<hash>\w{40}) (?P<user>[^<]{1,}) <(?P<mail>\S{1,})> (?P<time>\d{8,15}) (?P<hour>\S{0,6}) (?P<commit>.{1,})'
            checked_url = [
                self.reformat_url(site_url) + '.git/logs/HEAD',
                self.reformat_url(site_url) + '.git/LOGS/HEAD'
            ]
            for url in checked_url:
                try:
                    request = self.session.get(url)
                    if not request.ok:
                        continue
                    tmp_text = self.space_replacer(request.text)
                    if re.search(re_search, tmp_text):
                        text = tmp_text
                        find = True
                        break
                except:
                    pass

            if not find:
                return None

            return_lst: List[FirstHash] = list()
            for string in text.split('\n'):
                r_data = re.search(re_search, string.replace('\n', ''))
                if r_data:
                    return_lst.append(FirstHash(
                        r_data.group('first_hash'),
                        r_data.group('hash'),
                        r_data.group('user'),
                        r_data.group('mail'),
                        r_data.group('time'),
                        r_data.group('hour'),
                        r_data.group('commit')
                    ))
            return return_lst

        except:
            print(traceback.format_exc())
            return None

    def parseTreeHash(self, site: str, _hash : str) -> List[SimpleGitObject]:
        try:
            if not self.downloadObject(site, _hash):
                print('not download')
                return None
            tmp = self.getObjectData(_hash)
            r = re.search(r'tree (?P<hash>\S{40})', self.space_replacer(tmp))
            if not r:
                print('not found r')
                return None

            self.downloadObject(site, r.group('hash'))
            tmp = self.getObjectData(r.group('hash'))
            if not tmp:
                print('not found tmp')
                return None

            returnList = self._parseTreeHash(tmp)

            return returnList

        except:
            print(traceback.format_exc())
            return None

    def _parseTreeHash(self, text : str) -> List[SimpleGitObject]:
        returnList = list()
        for i in self.space_replacer(text).split('\n'):
            r = re.search("\d{1,10} (?P<fType>\S{4}) (?P<hash>\S{40}) (?P<fName>.{1,})", i)
            if r:
                if r.group('fType') not in ['tree', 'blob']:
                    continue
                returnList.append(SimpleGitObject(
                    GitObjectType.tree if r.group('fType') == 'tree' else GitObjectType.blob,
                    r.group('hash'),
                    r.group('fName')
                ))

        return returnList

    def downloadObject(self, site: str, _hash: str) -> bool:
        try:
            url = f'{self.reformat_url(site)}.git/objects/{_hash[:2]}/{_hash[2:]}'
            request = self.session.get(url)
            if not request.ok:
                return None

            request.encoding = 'utf-8'
            try:
                os.mkdir(f'objects/{_hash[:2]}')
            except:
                pass
            with open(f'objects/{_hash[:2]}/{_hash[2:]}', 'wb') as f:
                f.write(request.content)
            return True
        except:
            return False

    def getObjectData(self, _hash : str) -> str:
        try:
            return subprocess.getoutput(f'git cat-file -p {_hash}')
        except:
            return None

    def dumpHash(self, _hash : str):
        try:
            text = subprocess.getoutput(f'git cat-file -p {_hash}')
            with open(f'../tmp/{crud.getFileNameByHash(_hash)}', 'w', encoding='utf-8') as f:
                f.write(text)
        except:
            try:
                os.system(f'git cat-file -p {_hash} > ../tmp/{crud.getFileNameByHash(_hash)}')
            except:
                pass

    # dev tools
    def reformat_url(self, url : str) -> str:
        site_url = url if '://' in url else 'https://' + url
        site_url += '/' if not site_url.endswith('/') else ''
        return site_url

    def space_replacer(self, text : str) -> str:
        t = ''
        for i in text.split('\n'):
            t += re.sub(r'\s{1,}', ' ', i) + '\n'
        if t[-1] == '\n':
            t = t[:-1]
        return t



