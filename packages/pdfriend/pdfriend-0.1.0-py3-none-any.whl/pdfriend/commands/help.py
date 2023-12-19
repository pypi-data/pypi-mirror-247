
intro = """pdfriend: a command line utility for easily modifying PDF files
    usage: pdfriend [command] [arguments?] (note that options in [] are required and options in [?] are not)
    the following commands are available:
    """

outro = """use pdfriend help [command] to get the instructions for particular commands"""

help_blurbs = {
    "version":"""pdfriend version | -v | --version
    prints the current version of pdfriend
    """,
    "help": """pdfriend help [command?]
        display help message. If given a command, it will only display the help message for that command.
    """,
    "merge": """pdfriend merge [filename1] [filename2?] ... [-o|--outfile outfile?=pdfriend_output.pdf] [-q|--quality quality?=100]

merges the given files into one pdf. It can handle multiple pdfs, as well convert and merge png and jpg images. Glob patterns are also supported. You can specify the output filename using the -o or --outfile flag, otherwise it defaults to pdfriend_output.pdf. You can also specify the quality when images are converted to pdfs via the -q or --quality flag. It's an integer going from 0 to 100, 100 is no lossy compression and 0 is full lossy compression.

    examples:
        pdfriend merge pdf1.pdf img.png pdf2.pdf -o merged.pdf
            merges all of those into merged.pdf, preserving the quality of img.png
        pdfriend merge folder_name/* -o merged.pdf -q 50
            merges all files in directory folder_name into merged.pdf and compresses the images by 50%.
        pdfriend merge pdf1.pdf folder_name/* img.jpg pdf2.pdf -o apricot.pdf
            merges every file given, including all files in folder_name, into apricot.pdf
    """,
    "edit": """pdfriend edit [filename]
        edit the selected file in place, using a set of subcommands. After launching the edit shell, you can type h or help to list the subcommands.
    """,
    "invert": """pdfriend invert [filename] [-o|--outfile outfile?=pdfriend_output.pdf]
        create a PDF file with the pages of the input file, but in inverted order.

        examples:
            pdfriend invert puppy.pdf -o puppy-inv.pdf
                inverts the pages of puppy.pdf and saves to puppy-inv.pdf
    """,
    "clear": """pdfriend clear
        clears the pdfriend cache.
    """,
}


def help(command: str):
    try:
        print(help_blurbs[command])
    except KeyError:
        print(intro)
        print("\n".join([f"    {blurb}" for blurb in help_blurbs]), "\n")
        print(outro)
