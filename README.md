# Current development status: alpha test. Win10 is supported only

This python script automatically encrypts and synchronizes file on a filesystem. Синхронизация двустороняя - локальные заметки закачиваются в репозиторий, репозиторные заметки скачиваются в локальные

# About

This script is a very geeky way to synchronize your files between devices. It uses git as a remote storage and gpg as an encrypt engine. First installation is very painful, because it have to have gpg keys generated, backed up. Git repo should also be configured. Android sync is supported by installing Termux emulator. 

# Features

- No external libraries.
- Only changed files are handled.
- Encryption.
- Versioning with git.

# Encryption

- Encryption is done by delegating call to gpg tool.
- Files are encrypted locally, placed to a git repo and then committed
- Local files are stored with no encryption. If somebody gets access to the local device, files will be compromised.

# System requirements

- Windows 7/8/10.
- Python 3 is installed.
- git installed (start > cmd > git --version).
- gpg installed (start > cmd > gpg --version).
- gpg key is generated (gpg --gen-key).

# Installation

- Clone script.
- install latest version of CLI gnupg
- generate gpg keys and backup them to secure place
- install latest version of CLI git
- create remote repo and set it to /conf/default.conf
- gpg --edit-key my@example.com > trust > trust ultimately > yes > save

# Android installation

- install termux
- install gpg on termux: pkg install gpg
- install git on termux: pkg install git
- customize git: git config [--global] user.email "you@example.com"
- customize git: git config [--global] user.name "Your Name"
- (optional) customize git: git config credential.helper 'cache --timeout=300'
- gpg --edit-key my@example.com > trust > trust ultimately > yes > save

# Caveats

- To enable support of cyrillic characters, do the following: Region Settings > Additional date, time & regional settings > change date, time or number formats > administrative > change system locale > Beta: Use unicode UTF-8 for worldwide language support > Enable checkbox

# Technical aspects

- Первичная синхронизация выполняется, если отсутствует каталог .git в remote директории
- File unique identifier is file path.
- Modification or creation dates from filesystem metadata are not used in the script.
- Only file content and it's versions is used to resolve conflicts.
- Script runs only if remote repo is available.

# Limitations

- Asterisks in the file names are not supported.

# FAQ
- Если файл уже имеет расширение gpg, он будет зашифрован второй раз и будет иметь расширение myfile.txt.gpg.gpg

# Конфликтующие заметки

- Conflict resolve strategy: conflicted note from remote repo is renamed, copied to local catalog. Then both files are commited.
- Конфликт заметок сведен к минимуму, поскольку коммитятся только измененные файлы.
- Конфликтующий локальный файл переименовывается в имя_CURRENT_TIMESTAMP
- Conflicting file / folder with the same names: handled by 

## Конфликтующие заметки
Конфликтующая заметка - это файл, который при копировании на другую сторону встречает такой же файл.
- Конфликтующий локальный файл переименовывается в %FILENAME%_CURRENT_TIMESTAMP
- Точка возникновения конфликта - склонировал репозиторий, а файл в НЕрепозитории конфликтует с тем что находится в склонированном репозитории

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