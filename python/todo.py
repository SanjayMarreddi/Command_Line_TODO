"""
Author : Sanjay Marreddi
Date   : 23rd December 2020

This file contains code for implementing a command-line (CLI) program that
lets user's manage their todos.
Ihis is written as a part of `CoronaSafe Engineering Fellowship` Test.
"""


# Importing the required Modules.
import sys
from datetime import date


class Todo:

    """
    A class used to represent the command-line (CLI) program
    that lets you manage your todos.

    Attributes
    ----------
    CLI_Usage : str
        It lists the commands and their usage in CLI program.

    Methods
    -------

    Help()
        Prints the CLI Todo usage.

    List()
        Prints the todos that are not yet complete.
        The most recently added todo will be displayed first.

    Add()
        Adds the text of the todo item to the file for storing.

    Delete()
        Removes a Todo item by the number provided.

    Done()
        Marks a todo item as completed by the number provided.

    Report()
        Prints the latest tally of pending and completed todos.

    """

    CLI_Usage = \
        """Usage :-
$ ./todo add \"todo item\"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics"""

    def __init__(self):

        # Command is executed without any arguments
        if (len(sys.argv) == 1):

            # Encoding into `utf8` and printing the CLI Usage.
            sys.stdout.buffer.write(Todo.CLI_Usage.encode('utf8'))

    def Help(self):

        # Command is executed with `help` argument

        # Encoding into `utf8` and printing the CLI Usage.
        sys.stdout.buffer.write(Todo.CLI_Usage.encode('utf8'))

    def List(self):

        try:
            Todo_file = open("todo.txt")

            content = Todo_file.readlines()

            # Removing whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]

            if len(content) == 0:
                print("There are no pending todos!")

            todos = ""

            # Concatenating the text in the file in specified way
            for i in range(len(content), 0, -1):
                todos += "[{}]".format(i) + " " + content[i-1] + "\n"

            # Encoding into `utf8` and listing all the pending todos.
            sys.stdout.buffer.write(todos.encode('utf8'))

            Todo_file.close()

        except IOError:
            print("There are no pending todos!")

    def Add(self):

        # Command is executed with the text of the todo item.
        if (len(sys.argv) == 3):

            # Grabbing the text inputted.
            todo_text = sys.argv[2]

            # Opening the File in Append mode and writing into it.
            Todo_file = open("todo.txt", "a")
            Todo_file.write(todo_text+"\n")
            Todo_file.close()

            print("Added todo: " + '"{}"'.format(todo_text))

        else:
            print("Error: Missing todo string. Nothing added!")

    def Delete(self):

        # Command is executed with the number of the todo item to be deleted.
        if (len(sys.argv) == 3):

            line_to_remove = sys.argv[2]

            # Opening the File in both Read & Write Modes.
            with open("todo.txt", "r+") as Todo_file:

                content = Todo_file.readlines()
                Todo_file.seek(0)
                tracker = 0

                # Writing all the lines except the one to be removed.
                for current_line_no in range(1, len(content)+1):

                    if (current_line_no != int(line_to_remove)):

                        tracker += 1
                        Todo_file.write(content[current_line_no-1])

                Todo_file.truncate()

            if (tracker != len(content)):
                print("Deleted todo #{}".format(line_to_remove))

            # Attempting to delete a non-existent todo item
            if tracker == len(content):
                print("Error: todo #{} does not exist. Nothing deleted."
                      .format(line_to_remove))

        else:
            print("Error: Missing NUMBER for deleting todo.")

    def Done(self):

        # Command is executed with the no of todo item to be marked done.
        if (len(sys.argv) == 3):

            line_to_remove = sys.argv[2]
            text = ""

            # Opening the File in both Read & Write Modes.
            with open("todo.txt", "r+") as Todo_file:

                content = Todo_file.readlines()
                Todo_file.seek(0)
                current_line_no = 1

                for each_line in content:

                    # Writing all the lines except the one to be removed.
                    if (current_line_no != int(line_to_remove)):
                        Todo_file.write(each_line)

                    # The line to be removed is stored in `text` for later use.
                    if (current_line_no == int(line_to_remove)):
                        text = each_line

                    current_line_no += 1

                Todo_file.truncate()

            # Writing the todo item removed into Done file in specified Way.
            Done_file = open("done.txt", "a")
            Done_file.write("x " + str(date.today()) + " " + text)

            if (len(text) != 0):
                print("Marked todo #{} as done.".format(line_to_remove))

            # Attempting to mark a non-existed todo item as completed.
            else:
                print("Error: todo #{} does not exist.".format(line_to_remove))

        else:
            print("Error: Missing NUMBER for marking todo as done.")

    def Report(self):

        # Command is executed with `report` argument

        with open("todo.txt") as Todo_file:
            content = Todo_file.readlines()

        Todo_len = len(content)     # Storing the number of lines

        with open("done.txt") as Done_file:
            content_2 = Done_file.readlines()

        Done_len = len(content_2)   # Storing the number of lines

        print("{} Pending : {} Completed : {}".format(
            str(date.today()), Todo_len, Done_len))


# Creating an object of our class.
test_todo = Todo()

# Storing the number of arguments passed while running the file.
no_of_args = len(sys.argv)

# When more than 1 arguments are present, Call Methods based on the command.
if (no_of_args > 1):

    command = sys.argv[1]

    if (command == "help"):
        test_todo.Help()

    elif (command == "add"):
        test_todo.Add()

    elif (command == "ls"):
        test_todo.List()

    elif (command == "del"):
        test_todo.Delete()

    elif (command == "done"):
        test_todo.Done()

    elif (command == "report"):
        test_todo.Report()

    else:
        print("Error: Incorrect Command ! Try `help` command ")
