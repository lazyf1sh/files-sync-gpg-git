# Current development status: work in progress. Script is unstable.
This python script automatically encrypts and synchronizes file on a filesystem. Синхронизация двустороняя - локальные заметки закачиваются в репозиторий, репозиторные заметки скачиваются в локальные

# System requirements
- Python 3 installed
- git installed (start > cmd > git --version)
- gpg installed (start > cmd > gpg --version)
- gpg key is generated (gpg --gen-key)
- OS Windows

# Current features
- no external libs
- only changed files are handled

# Roadmap
- viewing file history based on git repo
- viewing deleted files based on git repo
- desktop / mobile frontend to prevent having unencrypted the notes at the filesystem. Frontend just runs python script.
- 

# Warning
Локальные заметки хранятся в незашифрованном виде. Если кто-то получит доступ к вашему устройству, на котором хранятся данные, заметки будут скомпрометированы.


# Как работает
- Первичная синхронизация выполняется, если отсутствует каталог .git в remote директории
- File unique identifier is file path
- No dates are used to resolve conflicts
- Only file content and it's versions is used to resolve conflicts:wq

# Ограничения
- Звёздочки в именах файлах не поддерживаются и будут убраны

# Roadmap
- [+] Files that have different contents only are objects to operations
- [] Синхронизация двустороняя - локальные заметки закачиваются в репозиторий, репозиторные заметки скачиваются в локальные
- [] Программа выполняется если установлена версия git не ниже той что была у меня на момент разработки
- [] Программа выполняется если установлена версия gpg не ниже той что была у меня на момент разработки
- [] Программа выполняется если есть права на запись и удаление файлов в оба каталога
- [] делать коммит если доступен репозиторий (скачивать какую-нибудь инфу с удаленного репозитория)
- [] делать коммит только после успешного pull
- [] коммитятся все файлы, кроме тех, которые имеют расширение .gpg
- [] Если в репозиторий подложить незашифрованный файл, то при первой синхронизации файл зашифруется и удалится с сервера
- [] Если файл уже имеет расширение gpg, он будет зашифрован второй раз и будет иметь расширение myfile.txt.gpg.gpg


# Конфликтующие заметки
- Conflict resolve strategy: conflicted note from remote repo is renamed, copied to local catalog. Then both files are commited.
- Конфликт заметок сведен к минимуму, поскольку коммитятся только измененные файлы.
- Конфликтующий локальный файл переименовывается в имя_CURRENT_TIMESTAMP
- Conflicting file / folder with the same names: handled by 

# Шифрование
- шифрование выполнено путем делегирования задачи команде gpg 
- файлы шифруются на локальной машине, кладутся в папку с гит-репозиторием коммитятся
- 

## Конфликтующие заметки
Конфликтующая заметка - это файл, который при копировании на другую сторону встречает такой же файл.
- Конфликт заметок сведен к минимуму, поскольку коммитятся только измененные файлы.
- Конфликтующий локальный файл переименовывается в %FILENAME%_CURRENT_TIMESTAMP

### Точки возникновения конфликтов
- Склонировал репозиторий, а файл в НЕрепозитории конфликтует с тем что находится в склонированном репозитории


# Programming todos
- remove leading slash from state tree element
- get rid of gpg extension in remote repo
- [] Программа выполняется если установлена версия gpg не ниже той что была у меня на момент разработки
- [] Программа выполняется если установлена версия git не ниже той что была у меня на момент разработки
- [] Программа выполняется если есть права на запись и удаление файлов в оба каталога
- [] делать коммит если доступен репозиторий (скачивать какую-нибудь инфу с удаленного репозитория)
- [] делать коммит только после успешного pull
- [] коммитятся только те файлы, которые имеют расширение .gpg
- [] При конфликте, конфликтующая заметка переименовывается и коммитятся обе заметки 
- [] Если в репозиторий подложить незашифрованный файл, то при первой синхронизации файл зашифруется и удалится с сервера

# troubleshooting
```
gpg: C19EFEA3CFA2D76F: There is no assurance this key belongs to the named user

- нужно выполнить
gpg --edit-key <YOUR_KEY>
trust
5 = I trust ultimately
yes
save

gpg --list-keys:
uid           [ultimate] notes <YOUR_KEY>
```