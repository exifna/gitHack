# GitHacker

## Данная утилита создана чтобы помочь тестировать различные информационные системы на безопасность, в частности на уязвимость получения исходного кода ресурса при наличии открытой папки .git/

## Как это работает? Почитать о сути этой уязвимости можно [тут](https://medium.com/nuances-of-programming/%D0%BF%D1%80%D0%BE%D1%81%D1%82%D0%BE%D0%B9-%D1%81%D0%BF%D0%BE%D1%81%D0%BE%D0%B1-%D0%B2%D0%B7%D0%BB%D0%BE%D0%BC%D0%B0-%D1%81%D0%B0%D0%B9%D1%82%D0%B0-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B5%D0%B3%D0%BE-git-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-5beed20619ee).

## Установка. Все команды надо вводить в терминал/cmd.

> `git clone https://github.com/exifna/gitHack.git`
> 
> `cd gitHack`
> 
> `pip install -r requirements.txt`
> 
> `mkdir gitFiles`
> 
> `cd gitFiles`
> 
> `mkdir tmp dumps`
> 
> `git init`
> 
> `python console.py`

## Прокси

> Прокси надо вводить в формате type://ip:port или type://login:password@ip:port
> 
> Пример tor прокси: `socks5://127.0.0.1:9050`

## Триггер-файлы
> В триггер файлы вы можете занести названия файлов, которые по вашему мнению содержат интересную вам информацию.
> 
> Пример:
> ```
> config.php
> wp-config.php
> settings.php
> cron.php 
> ```


## Функционал
- [x] Получение первоначальных хешей деревьев и их сканирование
- [x] Рекурсивное скачивание всех доступных (и получение информации о недоступных) файлах/папках с сайта 
- [x] Поиск по скачанным файлам по названию/расширению/хешу
- [ ] Просмотр триггер файлов определённого сайта
- [ ] Dump всех скачанных файлов в папку (считай дамп исходников сайта)
- [ ] Конфигурация через консоль
- [ ] Google autosearch







