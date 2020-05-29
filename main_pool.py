
from multiprocessing import Pool
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
import re
import concurrent.futures
import pdfplumber

regex = r"(CC|CcC|TI)+\s+([0-9]+)"
regex_dos = r"([0-9]+)(\s)([\d|»]{1})\n(IDEN)"
regex_tres = r"([0-9]+)(\n)(IDENTIFICACION)"



entries = os.listdir('archivos/')


def renombrar(entry):
    regex = r"(CC|CcC|TI)+\s+([0-9]+)"
    regex_dos = r"([0-9]+)(\s)([\d|»]{1}+)\n(IDEN)"
    regex_tres = r"([0-9]+)(\n)(IDENTIFICACION)"

    # Path of the pdf
    PDF_file = f"./archivos/{entry}"
    ''' 
    Part #1 : Converting PDF to images 
    '''

    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_file, 500)
    # Counter to store images of each page of PDF to image
    image_counter = 1
    # Iterate through all the pages stored above

    filename = "page_1.jpg"

    # Save the image of the page in system
    # pages[0].save(filename, 'JPEG')

    # Increment the counter to update filename
    image_counter = image_counter + 1



    # Recognize the text as string in image using pytesserct
    #text = str(((pytesseract.image_to_string(Image.open(filename),lang="spa"))))
    custom_config = r'-l eng --psm 6'

    pdf = pdfplumber.open(f"./archivos/{entry}")
    page = pdf.pages[0]
    text = page.extract_text()
    print(text)
    pdf.close()

    # matches = re.findall(regex, text, re.MULTILINE)
    # matches_dos = re.findall(regex_dos, text, re.MULTILINE)
    # matches_tres = re.findall(regex_tres, text, re.MULTILINE)


    # if len(matches) > 0:
    #     new_file = f"CC{matches[0][1]}_LB.pdf"
    #
    # if len(matches_dos) > 0:
    #     new_file = f"CC{matches_dos[0][0]}_LB.pdf"
    #
    # if len(matches_tres) > 0:
    #     new_file = f"CC{matches_tres[0][0]}_LB.pdf"
    #
    # os.rename(f"./archivos/{entry}", f"./archivos/{new_file}")

    return text



if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        for img_path, out_file in zip(entries, executor.map(renombrar, entries)):
            print(img_path, out_file, ', processed')
        