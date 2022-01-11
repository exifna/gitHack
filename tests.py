from src import crud
from src.gitTools import Git
from src.types import GitObjectType

proxy = 'socks5://127.0.0.1:9050'

git = Git(proxies={
    'http' : proxy,
    'https' : proxy
})

print(crud.get_config())