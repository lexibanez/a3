# Lex Ibanez
# laibanez@uci.edu
# 70063614

# testpath
# C:\Users\lexib\OneDrive\Desktop\ICS32\a2tests

from file_manager import *
from pathlib import Path
from Profile import Profile


edit_menu_options_list = ['-usr', '-pwd', '-bio', '-addpost', '-delpost', '-publish']
print_menu_options_list = ['-usr', '-pwd', '-bio', '-posts', '-post', '-all']


def run_ui(option):

    quit_flag = False

    while True:
        if quit_flag:
            return

        if option.lower() == 'c':
            directory = Path(input('Enter the directory where '
                                   'you would like to create the file: '))

            if directory.is_dir():
                try:
                    while True:
                        print('Enter your username: ', end='')
                        username = str(input()).strip()
                        status = check_input(username)
                        if not status:  # check if the username is valid
                            continue

                        print('Enter your password: ', end='')
                        password = str(input()).strip()
                        # check if the password is valid
                        status2 = check_input(password)
                        if not status2:
                            continue
                        # if both username and password are valid,
                        # break out of the loop
                        break
                    while True:
                        bio = str(input('Enter your bio: ')).strip('\'"')
                        status = check_spaces(bio)
                        if not status:
                            continue
                        break
                    while True:
                        file_name = str(input('Enter a name for '
                                              'the DSU file: ')).strip()
                        status = check_input(file_name)
                        if not status:
                            continue
                        break

                except Exception:
                    print("Could not make dsu file, please try again.")
                    break

                # if the file does not exist, create it
                if not (directory / (file_name + '.dsu')).exists():
                    dsu_path = create_file(directory, ['-n', file_name])
                    journal = Profile(None, username, password)
                    journal.bio = bio
                    journal.save_profile(dsu_path)
                    print("Dsu file created and currently open")

                # if the file exists, open it
                elif (directory / (file_name + '.dsu')).exists():
                    print("File already exists, opening file.")
                    try:
                        journal = open_dsu_file(directory/(file_name + '.dsu'))
                        journal.save_profile(directory / (file_name + '.dsu'))
                        dsu_path = directory / (file_name + '.dsu')
                    except Exception:
                        break

                while True:
                    print(f"\nCurrently looking at {file_name}.dsu,"
                          " please enter a journal command, "
                          "or 'Q' to close journal")
                    journal_menu_options()
                    command = input("Enter command: ").lower().strip()
                    while command not in ["e", "p", "q"]:
                        print("Invalid command, please try again.")
                        journal_menu_options()
                        command = input("Enter command: ").lower().strip()

                    args = []

                    if command == "e":
                        print(f"\nYou are now editing {file_name}.dsu,"
                              " please enter an editing command")
                        edit_menu_options()
                        option = input("Enter a command: ")
                        while option not in edit_menu_options_list:
                            print("Invalid command, please try again.")
                            edit_menu_options()
                            option = input("Enter a command: ")
                        args.append(option)
                        option_input = handle_edit_options(option, journal)
                        args.append(option_input)

                    elif command == "p":
                        print(f"\nYou are now looking at {file_name}.dsu, "
                              "please enter an print command")
                        print_menu_options()
                        option = input("Enter a command: ")
                        while option not in print_menu_options_list:
                            print("Invalid command, please try again.")
                            edit_menu_options()
                            option = input("Enter a command: ")
                        args.append(option)
                        option_input = handle_print_options(option, journal)
                        args.append(option_input)

                    if command == 'q':
                        quit_flag = True
                        break

                    edit_dsu_file(journal, dsu_path, command, args)
            else:
                print("Could not find the specified directory, "
                      "please try again.")

        elif option.lower() == 'o':
            while True:
                try:
                    directory = Path(input("Please enter the directory of"
                                           " the file you want to open: "))
                    journal = open_dsu_file(directory)
                    journal.save_profile(directory)
                    break
                except Exception:
                    print("Could not find the specified directory, or the "
                          "path provided is not a .dsu file."
                          "\nPlease try again.")

            while True:
                print(f"\nCurrently looking at {directory.name}, please "
                      "enter a journal command, or 'Q' to close journal")
                journal_menu_options()
                command = input("Enter command: ").lower().strip()
                while command not in ["e", "p", "q"]:
                    print("Invalid command, please try again.")
                    journal_menu_options()
                    command = input("Enter command: ").lower().strip()

                args = []

                if command == "e":
                    print(f"\nYou are now editing {directory.name}, "
                          "please enter an editing command")
                    edit_menu_options()
                    option = input("Enter a command: ")
                    while option not in edit_menu_options_list:
                        print("Invalid command, please try again.")
                        edit_menu_options()
                        option = input("Enter a command: ")
                    args.append(option)
                    option_input = handle_edit_options(option, journal)
                    args.append(option_input)

                elif command == "p":
                    print(f"\nYou are now looking at {directory.name}, "
                          "please enter an print command")
                    print_menu_options()
                    option = input("Enter a command: ")
                    while option not in print_menu_options_list:
                        print("Invalid command, please try again.")
                        edit_menu_options()
                        option = input("Enter a command: ")
                    args.append(option)
                    option_input = handle_print_options(option, journal)
                    args.append(option_input)

                if command.lower() == 'q':
                    quit_flag = True
                    break

                edit_dsu_file(journal, directory, command, args)


def journal_menu_options():
    print("-------------------------------------")
    print("E: Edit the current file")
    print("P: Print contents of the current file")
    print("Q: Quit editing menu")
    print("-------------------------------------")


def edit_menu_options():
    print("-------------------------------------")
    print("-usr: change your username")
    print("-pwd: change your password")
    print("-bio: change your bio")
    print("-addpost: make a post")
    print("-delpost: delete a post")
    print("-publish: publish to a server")
    print("-------------------------------------")


def print_menu_options():
    print("-------------------------------------")
    print("-usr: display your username")
    print("-pwd: display your password")
    print("-bio: display your bio")
    print("-posts: display all of your posts")
    print("-post: display a certain post")
    print("-all: display your whole profile")
    print("-------------------------------------")


def handle_edit_options(option, journal):
    if option == '-usr':
        while True:
            username = input("Enter your new username: ").strip()
            status = check_input(username)
            if not status:
                continue
            break
        return username
    if option == '-pwd':
        while True:
            password = input("Enter your new password: ").strip()
            status = check_input(password)
            if not status:
                continue
            break
        return password
    if option == '-bio':
        while True:
            bio = input("Enter your new bio: ").strip()
            if bio == '':
                print('Bio cannot be empty')
                continue
            if bio.isspace():
                print('Bio cannot be only spaces')
                continue
            break
        return bio
    if option == '-addpost':
        while True:
            post_content = input("Enter the content of your post: ")
            status = check_spaces(post_content)
            if not status:
                continue
            break
        return post_content
    if option == '-delpost':
        while True:
            get_all_posts(journal)
            id = input("Enter the id of the post you would like to delete: ")
            if not id.isdigit():
                print("ID must be a number")
                continue
            status = check_input(id)
            if not status:
                continue
            break
        return int(id)
    if option == '-publish':
        while True:
            get_all_posts(journal)
            id = input("Enter the id of the post you would like to publish: ")
            if not id.isdigit():
                print("ID must be a number")
                continue
            status = check_input(id)
            if not status:
                continue
            break
        return id


def handle_print_options(option, journal):
    if option == '-usr':
        return
    if option == '-pwd':
        return
    if option == '-bio':
        return
    if option == '-posts':
        return
    if option == '-post':
        while True:
            get_post_indexes_only(journal)
            id = input("Enter the id of the post you would like to view: ")
            status = check_input(id)
            if not status:
                continue
            elif not id.isdigit():
                print("Post id must be a number")
                continue
            break
        return id
    if option == '-all':
        return


def get_all_posts(journal):
    posts = journal.get_posts()
    i = 0
    for post in posts:
        print(f'{i}: {post["entry"]}')
        i += 1


def get_post_indexes_only(journal):
    posts = journal.get_posts()
    i = 0
    for post in posts:
        print(f'{i}:')
        i += 1
