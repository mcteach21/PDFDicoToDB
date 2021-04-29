import io
import os
import re

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def clean(toclean, title0):
    return toclean.replace('\n', '').replace(';', '\n').replace(title0 + ', ', '').replace(title0 + ' :', '').replace(
        title0, '').replace('r\'', 'ɣ')


def tofile(title, definition):
    print('add to file..{}'.format(title))
    with open(os.path.join('', f'pdf_content.txt'), 'ab') as file:
        line = '\n' + title + '\n\t' + definition
        file.write(line.encode('utf-8'))


def todatabase(title, definition):
    print('add to database..{}'.format(title))
    # dao.insert(title, definition.encode('utf-8'))


extracted = {}


def extract(data, letter):
    parts = re.split('[.\\n]+' + letter + '[\,]*', data)
    for part in parts:
        part = letter + part
        titles = re.findall('' + letter + '[^A-Z\d ][\w]*', part)
        if len(titles) > 0:
            title = titles[0]
            definition = clean(part, title)

            if len(definition) <= 255:
                if title.startswith(letter) and letter not in extracted:
                    extracted.update({title: definition})
                    print(title + ' ' + str(len(definition)))

            # print(title + ' ' + str(len(definition)))
            # print(definition)

            tofile(title, definition)
            todatabase(title, definition)


def process(path):
    fp = open(path, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()

    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    dico = {'A': range(18, 35), 'B': range(38, 51), 'C': range(50, 81), 'D': range(75, 96),
            'E': range(96, 116), 'É': range(96, 116), 'F': range(116, 130), 'G': range(130, 138),
            'H': range(138, 144),
            'I': range(144, 154), 'J': range(154, 156), 'L': range(156, 164),
            'M': range(164, 180), 'N': range(180, 186), 'O': range(186, 190), 'P': range(190, 214),
            'Q': range(214, 218), 'R': range(218, 234), 'S': range(234, 248), 'T': range(248, 260),
            'V': range(262, 270)
            }

    print('=================================================')

    for item in dico.items():
        # read_page(read_pdf, item[0], item[1])

        letter = item[0]
        letter_range = item[1]

        # for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
        for pageNumber, page in enumerate(PDFPage.get_pages(fp, check_extractable=True, caching=True)):

            if pageNumber in letter_range:
                print('==========================================')
                # print('page :  ' + str(pageNumber) + ' => ' + letter)
                # print('==========================================')

                interpreter.process_page(page)
                data = retstr.getvalue()
                # print(data)
                extract(data, letter)
                print('==========================================')

    for item in extracted.items():
        print(item[0] + ' ' + item[1])

    print('=================================================')
    print(len(extracted))
    print('=================================================')


# r'C:\Users\mchouarbi\Desktop\frkab\dallet_dico_fr_kab.pdf'
# r'C:\Users\mchouarbi\Desktop\frkab\Agemmay-n-Tmazight.pdf'

if __name__ == '__main__':
    path = r'C:\Users\mchouarbi\Desktop\BURO\ALL\frkab\dallet_dico_fr_kab.pdf'
    process(path)
