import configparser
from typing import List
from src.database import session
from src.gitTools import Git
from src.tables import *


def get_my_sites(session = session) -> List[Site]:
    return session.query(Site).order_by(-Site.id).all()

def get_interested_files(session = session) -> List[str]:
    return [x.name for x in session.query(InterestedFileName).all()]

def get_project_files_count(site_id : int, session = session) -> int:
    return session.query(GitObject).filter(GitObject.site_id == site_id).filter(GitObject.object_type == GitObjectType.blob.value).count()

def get_interested_files_count(site_id : int, session = session) -> int:
    tmp = 0
    data = session.query(GitObject).filter(
        GitObject.site_id == site_id
    ).all()
    for i in data:
        if i.name in get_interested_files():
            tmp += 1

    return tmp

def remove_site(site_id : int,session = session):
    [session.delete(x) for x in session.query(GitObject).filter(GitObject.site_id == site_id).all()]
    session.delete(session.query(Site).filter(Site.id == site_id).one())
    session.commit()



def get_last_sites(session = session) -> List[Site]:
    return session.query(Site).order_by(-Site.id).limit(10).all()

def find_sites(string:str, session = session) -> List[Site]:
    return session.query(Site).filter(Site.site_name.startswith(string)).order_by(-Site.id).limit(10).all()

def get_triggers_site_files(site_id : int, session = session) -> List[GitObject]:
    result = list()
    for i in get_interested_files():
        result.extend(session.query(GitObject).filter(GitObject.site_id == site_id).filter(GitObject.name == i).all())

    return result


def add_site(site_name: str, session = session) -> Site:
    site = Site(
        site_name=site_name
    )
    session.add(site)
    session.commit()
    return site

def get_folder_data(site_id: int, folder: str, session = session) -> List[GitObject]:
    return session.query(GitObject).filter(GitObject.site_id == site_id).filter(
        GitObject.path == folder
    ).all()

def find_objects_by_data(site_id: int, data: str, session = session) -> List[GitObject]:
    result = list()
    result.extend(session.query(GitObject).filter(GitObject.site_id == site_id).filter(GitObject.name.contains(data)).all())
    result.extend(session.query(GitObject).filter(GitObject.site_id == site_id).filter(GitObject.path.contains(data)).all())
    result.extend(session.query(GitObject).filter(GitObject.site_id == site_id).filter(GitObject._hash.contains(data)).all())
    return result


def get_site_objects_by_id(site_id: int, session = session) -> List[GitObject]:
    return session.query(GitObject).filter(GitObject.site_id == site_id).all()

def getFileNameByHash(_hash: str, session = session) -> str:
    return session.query(GitObject).filter(GitObject._hash == _hash).one().name

def get_site(site_id : int, session = session) -> Site:
    return session.query(Site).filter(Site.id == site_id).one_or_none()

def add_object(site_id : int, object_type: GitObjectType, download: bool, _hash: str, path: str, name : str, session = session):
    obj = GitObject(
        site_id = site_id,
        object_type = object_type,
        download = download,
        _hash = _hash,
        path = path,
        name = name
    )
    session.add(obj)
    session.commit()

def addTrigger(trigger : str, session = session):
    session.add(InterestedFileName(name = trigger))
    session.commit()

def deleteTrigger(trigger_id : int, session = session):
    session.delete(session.query(InterestedFileName).filter(InterestedFileName.id == trigger_id).one())
    session.commit()

def getTriggerData(session = session) -> List[InterestedFileName]:
    return session.query(InterestedFileName).all()

def editProxies(proxies : str):
    git = Git()
    parser = configparser.ConfigParser()
    parser['PROXIES'] = {'proxy' : proxies}
    with open('../../config.cfg', 'w', encoding='utf-8') as f:
        parser.write(f)



def get_config() -> dict:
    git = Git()
    parser = configparser.ConfigParser()
    parser.read('../../config.cfg')
    d = dict()
    d['proxies'] = parser['PROXIES']['proxy']

    return d
