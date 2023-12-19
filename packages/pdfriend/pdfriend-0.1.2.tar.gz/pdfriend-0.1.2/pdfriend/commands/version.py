import pkg_resources


def version():
    return pkg_resources.get_distribution("pdfriend").version
