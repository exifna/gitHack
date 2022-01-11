import os
import subprocess
import traceback
from datetime import datetime
from pick import pick
from src import crud, types
from src.gitTools import Git

title = types.label + 'Выбери с чем ты хочешь работать'
options = ['Мои сайты', 'Просканировать сайт', 'Конфигурация', 'Google AutoSearch']


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def recurser(site_id: int, _hash : str, path: str, name: str):
    try:
        proxy = crud.get_config()['proxies']
        proxies = {'http' : proxy, 'https' : proxy}
        git = Git(proxies=proxies)
        site = crud.get_site(site_id).site_name
        print(f'Качаю "{path}{name}"')
        obj = git.downloadObject(site, _hash)
        crud.add_object(site_id, types.GitObjectType.tree.value,  bool(obj), _hash, path, name)
        if not obj:
            return


        txt = git.getObjectData(_hash)
        if not txt:
            return

        for i in git._parseTreeHash(txt):
            if i.Type == types.GitObjectType.tree:
                recurser(site_id, i._hash, path + name + '/', i.name)

            if i.Type == types.GitObjectType.blob:
                if True in [i.name.endswith(x) for x in types.ignore]:
                    continue
                print(f'> Качаю {path + name}/{i.name}')
                t = git.downloadObject(site, i._hash)
                crud.add_object(site_id, types.GitObjectType.blob.value,  bool(t), i._hash, path + name + '/', i.name)
    except:
        print(traceback.format_exc().replace('\n', '   |   '))

def recurse_dump(site_id: int, path: str):
    print(f'> Check folder: {path}')
    for i in crud.get_folder_data(site_id, path):
        if i.object_type == types.GitObjectType.tree.value:
            try:
                os.mkdir(f'../dumps/{crud.get_site(site_id).site_name}{path}{i.name}')
                recurse_dump(site_id, path + i.name + '/')
            except:
                pass
        if i.object_type == types.GitObjectType.blob.value:
            print(f'> Dump {i.path}{i.name}...')
            if not i.download:
                text = '-'
                with open(f'../dumps/{crud.get_site(site_id).site_name}{path}{i.name}', 'w', encoding='utf-8') as f:
                    f.write(text)
            else:
                git = Git()
                try:
                    text = subprocess.getoutput(f'git cat-file -p {i._hash}')
                    with open(f'../dumps/{crud.get_site(site_id).site_name}{path}{i.name}', 'w', encoding='utf-8') as f:
                        f.write(text)

                except:
                    try:
                        os.system(f'git cat-file -p {i._hash} > ../dumps/{crud.get_site(site_id).site_name}{path}{i.name}')

                    except:
                        print(f'> Can\'t dump {i.path}{i.name} | {i._hash}')



while True:

    option, index = pick(options, title, indicator='=>')

    if index == 0:
        while True:
            tmp_data = crud.get_my_sites()
            sites = ['Назад'] + [x.site_name for x in tmp_data]
            option, index = pick(sites, types.label + 'Выбери сайт', indicator='=>')
            options_ = ['Назад'] + ['Просмотр всех файлов', 'Поиск файлов по любой информации', 'Просмотр триггер-файлов' ,
                                    'Dump всех скачанных файлов в папку', 'Удалить всю информацию']
            if not index:
                break

            clear()
            print(types.label + '=> Плыз вейт, подгруражаю информацию...')
            site_name = tmp_data[index - 1].site_name
            site_id = tmp_data[index-1].id
            txt = str(types.label +
                f'\n=> Ты работаешь с сайтом {site_name}'
                f'\n=> Файлов найдено: {crud.get_project_files_count(tmp_data[index - 1].id)}'
                f'\n=> Файлов с триггер названиями: {crud.get_interested_files_count(tmp_data[index - 1].id)}')

            while True:

                option, index_ = pick(options_, txt, indicator='=>')
                if not index_:
                    break

                if index_ == 1:
                        path = '/'
                        git = Git()
                        while True:
                            clear()
                            files = crud.get_folder_data(site_id, path)
                            option, index__ = pick(['Назад'] + [f'[{"+ скачан" if x.download else "- нету  "} {"/" if x.object_type == types.GitObjectType.tree.value else " "}] ' + str(x.path + x.name) + str("/" if x.object_type == types.GitObjectType.tree.value else "") for x in files], types.label + f'Выбери файл для просмотра', indicator='=>')

                            if not index__:
                                if path == '/':
                                    break
                                path = str('/'.join(path.split('/')[:-2]) + '/').replace('//', '/')
                                continue

                            if files[index__ - 1].object_type == types.GitObjectType.tree.value:
                                path = files[index__ - 1].path + files[index__ - 1].name + '/'
                                files = crud.get_folder_data(site_id, path)
                                continue

                            text = git.getObjectData(files[index__ - 1]._hash)
                            clear()
                            print_text = types.label + f'> Нажми <enter> чтобы выйти, или напиши download чтобы скачать файл.\n> {"=" * 65} <\n\n{text if text else "> Не удалось получить исходный код..."}\n\n> {"=" * 65} <\n> Нажми <enter> чтобы выйти, или напиши download чтобы скачать файл.\n(input)=> '
                            tmp = input(print_text)
                            clear()

                            if tmp == 'download':
                                print(types.label +  f'> Подожди, загружаю файл... После загрузки он должен был появится в папке gitFiles/tmp/ с названием "{files[index__ - 1].name}"')
                                git.dumpHash(files[index__ - 1]._hash)
                                input('> Дамп завершён... Нажми <enter> чтобы продолжить.')

                if index_ == 2: # поиск файла по информации
                    clear()
                    data = input(types.label  + f'> Введи любую известную тебе информацию о файле (хеш, имя, путь): ')
                    if not data:
                        continue

                    clear()
                    print(types.label +  '> Подожди, получаю данные от базы данных...')
                    files = crud.find_objects_by_data(site_id, data)
                    t = ['Назад'] + [f'[{"+ скачан" if x.download else "- нету  "} {"/" if x.object_type == types.GitObjectType.tree.value else " "}] ' + str(x.path + x.name) + str("/" if x.object_type == types.GitObjectType.tree.value else "") for x in files]
                    if not len(t):
                        clear()
                        input(types.label +  '> Ничего не найдено...')
                        break

                    _, index__ = pick(t, types.label + 'Выбери пункт, содержащий нужную тебе информацию. Уточнение: по папкам переходить нельзя', indicator='=>')

                    if not index__:
                        continue

                    if files[index__ - 1].object_type == types.GitObjectType.tree.value:
                        clear()
                        input(types.label + f'Путь: {files[index__ - 1].path + files[index__ - 1].name}/')
                        break

                    git = Git()
                    text = git.getObjectData(files[index__ - 1]._hash)
                    clear()
                    print_text = types.label + f'> Нажми <enter> чтобы выйти, или напиши download чтобы скачать файл.\n> {"=" * 65} <\n\n{text if text else "> Не удалось получить исходный код..."}\n\n> {"=" * 65} <\n> Нажми <enter> чтобы выйти, или напиши download чтобы скачать файл.\n(input)=> '
                    tmp = input(print_text)
                    clear()

                    if tmp == 'download':
                        print(types.label +  f'> Подожди, загружаю файл... После загрузки он должен был появится в папке gitFiles/tmp/ с названием "{files[index__ - 1].name}"')
                        git.dumpHash(files[index__ - 1]._hash)
                        input('> Дамп завершён... Нажми <enter> чтобы продолжить.')

                if index_ == 3:
                    files = crud.get_triggers_site_files(site_id)
                    t = ['Назад'] + [f'[{"+ скачан" if x.download else "- нету  "} {"/" if x.object_type == types.GitObjectType.tree.value else " "}] ' + str(x.path + x.name) + str("/" if x.object_type == types.GitObjectType.tree.value else "") for x in files]
                    if not len(t):
                        clear()
                        input(types.label +  '> Ничего не найдено...')
                        break

                    _, index__ = pick(t, types.label + 'Выбери пункт, содержащий нужную тебе информацию. Уточнение: по папкам переходить нельзя', indicator='=>')

                    if not index__:
                        continue

                    if files[index__ - 1].object_type == types.GitObjectType.tree.value:
                        clear()
                        input(types.label + f'Путь: {files[index__ - 1].path + files[index__ - 1].name}/')
                        break

                    git = Git()
                    text = git.getObjectData(files[index__ - 1]._hash)
                    clear()
                    print_text = types.label + f'> Нажми <enter> чтобы выйти, или напиши download чтобы скачать файл.\n> {"=" * 65} <\n\n{text if text else "> Не удалось получить исходный код..."}\n\n> {"=" * 65} <\n> Нажми <enter> чтобы выйти, или напиши download чтобы скачать файл.\n(input)=> '
                    tmp = input(print_text)
                    clear()

                    if tmp == 'download':
                        print(types.label +  f'> Подожди, загружаю файл... После загрузки он должен был появится в папке gitFiles/tmp/ с названием "{files[index__ - 1].name}"')
                        git.dumpHash(files[index__ - 1]._hash)
                        input('> Дамп завершён... Нажми <enter> чтобы продолжить.')

                if index_ == 4:
                    path = '/'
                    git = Git()
                    os.mkdir(f'../dumps/{crud.get_site(site_id).site_name}')
                    recurse_dump(site_id, path)
                    print('\n\n> Done.')



                if index_ == 5:
                    if input('> Вы уверены? ').lower() in ['y', 'yes', 'д', 'да']:
                        crud.remove_site(site_id)

                    break

    if index == 1:
        clear()
        site = input(types.label + '> Введи url сайта, который хочешь просканировать: ').split('://')[-1]
        if not site:
            continue

        proxy = crud.get_config()['proxies']
        proxies = {'http' : proxy, 'https' : proxy}
        git = Git(proxies=proxies)
        data = git.getFirstHashes(site)
        if not data:
            input('> Ничего не найдено...')
            continue

        _, index_ = pick(['Назад'] + [f'{x._hash} | {datetime.utcfromtimestamp(int(x.time)).strftime("%d-%m-%Y %H:%M:%S")} | {x.mail} | {x.commit_message}' for x in list(reversed(data))], types.label + '> Выбери дерево, с которым хочешь работать', indicator='=>')

        if not index_:
            continue

        s_data = crud.add_site(site)
        site_id = s_data.id
        site_name = s_data.site_name

        path = '/'
        first_hashes = git.parseTreeHash(site_name, data[index_-1]._hash)
        if not first_hashes:
            input('> Не удалось получить хеш дерева... (<enter>)')
            continue

        for i in first_hashes:
            try:
                if i.Type == types.GitObjectType.tree:
                   continue

                print(f'Скачивая файл "{i.name}"...    |   ', end="")
                t = git.downloadObject(site_name, i._hash)
                crud.add_object(site_id, i.Type.value, bool(t), i._hash, '/', i.name)
                print('Удалось' if t else 'Не удалось')
            except:
                print(f'Произошла ошибка: {traceback.format_exc()}. {i.name} - {i._hash}')

        for i in first_hashes:
            try:
                if i.Type == types.GitObjectType.tree:
                   recurser(site_id, i._hash, '/', i.name)
            except:
                print(f'Произошла ошибка: {traceback.format_exc()}. {i.name} - {i._hash}')

    if index == 2:
        actions = ['Назад', 'Триггер-файлы', 'Прокси']
        while True:
            option, index_ = pick(actions, types.label + f'> Выбери чтобы ты хотел просмотреть/изменить',
                                  indicator='=>')
            if index_ == 0:
                break

            if index_ == 1:
                while True:
                    data = crud.getTriggerData()
                    actions_ = ['Назад', 'Добавить триггер-файл'] + ['[*] ' + x.name for x in data]
                    option, index__ = pick(actions_, types.label + f'> Выбери какой триггер добавить', indicator='=>')
                    if not index__:
                        break

                    if index__ == 1:
                        clear()
                        t = input(types.label + '> Введи триггер (оставь строку пустой если хочешь отменить): ')
                        if not t:
                            continue

                        crud.addTrigger(t)
                        continue

                    clear()
                    if input(types.label + '> Подтверди удаление [y/д]: ').lower() in ['y', 'yes', 'д', 'да']:
                        crud.deleteTrigger(data[index__ - 2].id)

            if index_ == 2:
                clear()
                t = input(types.label + f'> Прокси сейчас: "{crud.get_config()["proxies"]}"\n> Введи новые прокси, если не хочешь, то оставь поле пустым: ')
                if not t:
                    continue

                crud.editProxies(t)











