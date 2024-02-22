# Lex Ibanez
# laibanez@uci.edu
# 70063614

from pathlib import Path
from Profile import Profile, Post, DsuProfileError
from ds_client import send


def get_last_option(options):
    if len(options) == 3:
        return options[2]
    elif len(options) == 4:
        return options[3]


def list_directory(directory, options):
    contents = list(directory.iterdir())
    # sort contents for files
    files = [x for x in contents if x.is_file()]
    # sort contents for directories
    directories = [x for x in contents if x.is_dir()]

    if '-e' in options:
        suffix = get_last_option(options)

        for file in files:
            if file.suffix == '.' + suffix:
                print(file)
        for directory in directories:
            if '-r' in options:
                list_directory(directory, options)

    elif '-s' in options:
        search_file = get_last_option(options)

        # checks if the search file has a path
        if Path(directory / search_file).is_file():
            print(Path(directory / search_file))
        for directory in directories:
            if '-r' in options:
                list_directory(directory, options)

    elif '-f' in options:
        for file in files:
            print(file)
        for directory in directories:
            if '-r' in options:
                list_directory(directory, options)

    else:
        for file in files:
            print(file)
        for directory in directories:
            print(directory)
            if '-r' in options:
                list_directory(directory, options)


def create_file(directory, options):
    if not directory.is_dir():
        print("not a directory")
        raise Exception("not a directory")

    if "-n" in options:
        index = options.index('-n')
        if index + 1 < len(options):
            file_name = options[index + 1]
            new_path = directory / f'{file_name}.dsu'
            new_path.touch()
        else:
            print("missing file name")
            raise Exception("missing file name")
    else:
        print("missing -n option")
        raise Exception("missing -n option")

    return new_path


def delete_file(directory):
    if directory.is_file():
        if directory.suffix == '.dsu':
            file_name = directory
            directory.unlink()
            print(f'{file_name} DELETED')
        else:
            print("ERROR")
    else:
        print("ERROR")


def read_file(directory):
    if directory.is_file():
        if directory.suffix == '.dsu':
            with open(directory, 'r') as file:
                content = file.read()
                if not content:
                    print("empty file")
                else:
                    print(content.strip())
        else:
            print("not a dsu file")
    else:
        print("not a file")


def open_dsu_file(directory):
    if directory.is_file():
        if directory.suffix == '.dsu':
            try:
                # instantiate a new profile object
                journal = Profile()
                # load the profile from the file system into the object
                journal.load_profile(directory)
                return journal
            except DsuProfileError:
                print("File does not follow Profile format.")
                raise Exception
        else:
            raise Exception("not a .dsu file")
    else:
        raise Exception("could not open the file")


def edit_dsu_file(journal: Profile, dsu_path: str, command=None, args=None):

    if command.lower() == 'q':
        return

    elif command.lower() == 'e':
        if '-usr' in args:
            username = get_argument_value(args, '-usr')
            journal.username = username
            journal.save_profile(dsu_path)
        if '-pwd' in args:
            pwd = get_argument_value(args, '-pwd')
            journal.password = pwd
            journal.save_profile(dsu_path)
        if '-bio' in args:
            bio = get_argument_value(args, '-bio')
            journal.bio = bio
            journal.save_profile(dsu_path)
        if '-addpost' in args:
            post_content = get_argument_value(args, '-addpost')
            post = Post(post_content)
            journal.add_post(post)
            journal.save_profile(dsu_path)
        if '-delpost' in args:
            for arg in args:
                if arg.isdigit():
                    index = int(arg)
                    break
            journal.del_post(index)
            journal.save_profile(dsu_path)
        if '-publish' in args:
            if journal.dsuserver is None:
                IP = input("Enter the server ip: ")
                journal.dsuserver = IP
                journal.save_profile(dsu_path)
            for arg in args:
                if arg.isdigit():
                    index = int(arg)
                    break
            post = journal.get_posts()[index]["entry"]
            send(journal.dsuserver, 3021, journal.username, journal.password, post, journal.bio)
        if '-publishbio' in args:
            new_bio = get_argument_value(args, '-publishbio')
            if journal.dsuserver is None:
                IP = input("Enter the server ip: ")
                journal.dsuserver = IP
                journal.save_profile(dsu_path)
            send(journal.dsuserver, 3021, journal.username, journal.password, None, new_bio)

        return

    elif command.lower() == 'p':
        if '-usr' in args:
            print(f'Your username is {journal.username}\n')
        if '-pwd' in args:
            print(f'Your password is {journal.password}\n')
        if '-bio' in args:
            print(f'Your bio is {journal.bio}\n')
        if '-posts' in args:
            get_all_posts(journal)
        if '-post' in args:
            try:
                id = get_argument_value(args, '-post')
                print(journal.get_posts()[int(id)]["entry"])
            except IndexError:
                print("Index out of bounds. Please try again.")
        if '-all' in args:
            print(journal.__str__())
            get_all_posts(journal)

        return


# get the value of the argument after the "-xxx" command including spaces
def get_argument_value(args, command):
    if command in args:
        start_index = args.index(command) + 1
        end_index = next((i for i,
                          arg in enumerate(args[start_index:],
                                           start=start_index)
                          if arg.startswith('-')), len(args))
        value = ' '.join(args[start_index:end_index])
        # get the value of the argument after the
        # "-xxx" command including spaces
        return value.strip('\'"')
    else:
        return None


def get_all_posts(journal):
    posts = journal.get_posts()
    i = 0
    for post in posts:
        print(f'{i}: {post["entry"]}\nTimestamp: {post["timestamp"]}')
        i += 1


def check_spaces(input):
    if input.isspace():
        print('Input cannot be only spaces')
        return False
    if input == '':
        print('Input cannot be empty')
        return False
    return True


def check_input(input):
    if input == '':
        print('Input cannot be empty')
        return False
    if ' ' in input:
        print('Input cannot contain spaces')
        return False
    if input.isspace():
        print('Input cannot be only spaces')
        return False
    return True
