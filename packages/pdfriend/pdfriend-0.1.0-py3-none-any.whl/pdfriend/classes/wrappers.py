import pypdf
import datetime
import pathlib
from typing import Self
from PIL import Image
from pdfriend.classes.platforms import Platform

class PDFWrapper:
    def __init__(self, pages: list[pypdf.PageObject] = None):
        self.pages = [] if pages is None else pages

    def __getitem__(self, num: int) -> pypdf.PageObject:
        return self.pages[num - 1]

    def __setitem__(self, num: int, page: pypdf.PageObject):
        self.pages[num - 1] = page

    @classmethod
    def Read(cls, filename: str):
        pdf = pypdf.PdfReader(filename)

        return PDFWrapper(pages=list(pdf.pages))

    def len(self):
        return len(self.pages)

    def rotate_page(self, page_num: int, angle: float) -> Self:
        int_angle = int(angle)
        if int_angle % 90 == 0:
            self[page_num].rotate(int_angle)
            return self

        rotation = pypdf.Transformation().rotate(angle)
        self[page_num].add_transformation(rotation)
        return self

    def pop_page(self, page_num: int) -> pypdf.PageObject:
        return self.pages.pop(page_num - 1)

    def swap_pages(self, page_num_0: int, page_num_1: int) -> Self:
        temp = self[page_num_0]
        self[page_num_0] = self[page_num_1]
        self[page_num_1] = temp

    def merge_with(self, other: Self) -> Self:
        self.pages.extend(other.pages)

        return self

    def invert(self) -> Self:
        self.pages = self.pages[::-1]

        return self

    # def interlace(self, other: Self) -> Self:
    #     return PDFWrapper()

    def write(self, filename: str):
        writer = pypdf.PdfWriter()
        for page in self.pages:
            writer.add_page(page)

        writer.write(filename)

    def backup(self, name: str | pathlib.Path) -> pathlib.Path:
        if not isinstance(name, pathlib.Path):
            name = pathlib.Path(name)

        now: str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        backup_file: pathlib.Path = Platform.NewBackup(
            f"{name.stem}_{now}.pdf"
        )

        self.write(backup_file)

        return backup_file


def convert_to_rgb(img_rgba: Image.Image):
    try:
        img_rgba.load()
        _, _, _, alpha = img_rgba.split()

        img_rgb = Image.new("RGB", img_rgba.size, (255, 255, 255))
        img_rgb.paste(img_rgba, mask=alpha)

        return img_rgb
    except (IndexError, ValueError):
        return img_rgba


class ImageWrapper:
    def __init__(self, images: list[Image.Image]):
        self.images = [convert_to_rgb(image) for image in images]

    @classmethod
    def FromFiles(cls, filenames: list[str]) -> Self:
        return ImageWrapper([Image.open(filename) for filename in filenames])

    def equalize_widths(self):
        max_width = max([image.size[0] for image in self.images])

        for i, image in enumerate(self.images):
            width, height = image.size

            scale = max_width / width

            self.images[i] = image.resize((max_width, int(height * scale)))

    def write(self, outfile: str, quality: int | float):
        self.images[0].save(
            outfile,
            "PDF",
            optimize=True,
            quality=int(quality),
            save_all=True,
            append_images=self.images[1:],
        )
