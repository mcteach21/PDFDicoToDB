from termcolor import colored
from menu import Menu
from option import Option
from dao import Dao
from pdfparser import process

msg_color = 'yellow'


def print_msg(msg):
    print('*******************************************************')
    print('\t', colored(msg, msg_color))
    print('*******************************************************')


def extract():
    path = r'pdfs\dallet_dico_fr_kab.pdf'
    process(path)


def search():
    word = input('mot recherché : ')
    result = dao.search(word)
    if not result:
        print('Aucune définition trouvée.')
    for definition in result:
        print('- {} [{}]'.format(definition[1], definition[0]))


if __name__ == '__main__':
    print_msg('Python : PDF => Dictionnaire')
    dao = Dao()
    menu = Menu([
        Option('Extraire fichier PDF (BD+Fichier)', extract),
        Option('Chercher dans Dictionnaire', search)
        # , Option('Tests', test)
    ])
    while not menu.want_exit:
        menu.show()
    print('*******************************************************')
