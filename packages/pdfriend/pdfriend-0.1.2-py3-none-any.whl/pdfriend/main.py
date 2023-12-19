import argparse
from pdfriend.classes.platforms import Platform
import pdfriend.commands as commands


def main():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")

    parser.add_argument("commands", type=str, nargs="*")

    parser.add_argument("-o", "--outfile", type=str, default="pdfriend_output.pdf")
    parser.add_argument("-q", "--quality", type=int, default=100)

    args = parser.parse_args()

    Platform.Init()

    command = ""
    if len(args.commands) > 0:
        command = args.commands[0]

    if command == "version" or args.version:
        print(commands.version())
    elif command == "help" or args.help:
        command_to_display = None
        if len(args.commands) >= 2:
            command_to_display = args.commands[1]

        commands.help(command_to_display)
    elif command == "merge":
        if len(args.commands) < 2:
            print("You need to specify at least one file or pattern to be merged")
            return

        commands.merge(args.commands[1:], args.outfile, args.quality)
    elif command == "edit":
        if len(args.commands) < 2:
            print("You need to specify a file for editing")
            return

        commands.edit(args.commands[1])
    elif command == "invert":
        if len(args.commands) < 2:
            print("You need to specify a file to be inverted")
            return

        commands.invert(args.commands[1], args.outfile)
    elif command == "swap":
        if len(args.commands) < 4:
            print("You need to specify a file and 2 pages to be swapped")
            return

        commands.swap(args.commands[1], args.commands[2], args.commands[3])
    elif command == "clear":
        commands.clear()
    else:
        print(f"command \"{command}\" not recognized")
        print("use pdfriend help for a list of the available commands")
