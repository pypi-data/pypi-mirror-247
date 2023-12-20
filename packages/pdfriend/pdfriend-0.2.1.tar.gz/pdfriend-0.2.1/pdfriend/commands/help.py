
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
    "invert": """pdfriend invert [filename] [-o|--outfile outfile?=pdfriend_output.pdf] [-i|--inplace?]
        create a PDF file with the pages of the input file, but in inverted order. Adding -i or --inplace will make it so the input file is modified, instead of creating a new one.

        examples:
            pdfriend invert puppy.pdf -o puppy-inv.pdf
                inverts the pages of puppy.pdf and saves to puppy-inv.pdf
            pdfriend invert kitty.pdf -i
                inverts the pages of kitty.pdf
    """,
    "clear": """pdfriend clear
        clears the pdfriend cache.
    """,
    "swap": """pdfriend swap [filename] [page_0] [page_1] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        swaps the specified pages in the PDF file. Adding -i or --inplace will make it so the input file is modified, instead of creating a new one.

        examples:
            pdfriend swap notes.pdf 1 3 -i
                swaps pages 1 and 3 in notes.pdf (modifies the file)
            pdfriend swap templ.pdf 6 3 -o new-templ.pdf
                swaps pages 6 and 3 and saves to new-templ.pdf
            pdfriend swap k.pdf 2 9
                swaps pages 2 and 9 and saves to pdfriend_output.pdf
    """,
    "remove": """pdfriend remove [filename] [pages] [-o|--outfile?=pdfriend_output.pdf] [-i|--inplace?]
        removes specified pages from the PDF file. Adding -i or --inplace will make it so the input file is modified, instead of creating a new one.

        examples:
            pdfriend remove input.pdf 6
                removes page 6 and saves to pdfriend_output.pdf
            pdfriend remove input.pdf 5,6,9 -o out.pdf
                removes pages 5,6,9 and saves to out.pdf
            pdfriend remove input.pdf 3-7 -o out
                removes pages 3 through 7 (INCLUDING 7) and saves to out.pdf
            pdfriend remove input.pdf 13,2,4-7,1 -i
                removes pages 1,2,4,5,6,7,13 from input.pdf (modifies the file)
    """,
}


def help(command: str):
    try:
        print(help_blurbs[command])
    except KeyError:
        print(intro)
        print("\n".join([f"    {blurb}" for blurb in help_blurbs]), "\n")
        print(outro)
