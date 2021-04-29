# Dao class
import mysql.connector
from mysql.connector import errorcode


class Dao:
    config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'database': 'dico_fr_kb',
        'raise_on_warnings': True
    }
    connection = None

    def __init__(self):
        print('dao..')
        if Dao.connection is None:
            self.connect_to_db()

    @staticmethod
    def connect_to_db():
        try:
            Dao.connection = mysql.connector.connect(**Dao.config)
            print('connection success!')
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('connection error (ER_ACCESS_DENIED_ERROR) : {}'.format(error.msg))
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print('connection error (ER_BAD_DB_ERROR) : {}'.format(error.msg))
            else:
                print(error.msg)

    # CRUD
    def execute(self, sql_command, args):
        cursor = self.connection.cursor()
        cursor.execute(sql_command, args)
        self.connection.commit()
        cursor.close()

    source_tables = [
        {'name':'Dictionnaire Kabyle-Francais J-M-Dallet', 'table':'dico_fr_kab_dallet_1985'},
        {'name':'Dictionnaire Kabyle-Francais Augustin Olivier 1878', 'table':'dico_kab_fr_ao_1878'}
    ]

    def search(self, word):
        definitions = []
        for source in self.source_tables:
            item = self.select('SELECT * FROM {} WHERE Mot = %(word_filter)s'.format(source['table']), {'word_filter': word})
            if item:
                definition = item[0][2]
                source_name = source['name']
                definitions.append([source_name, definition])

        return definitions

    def select(self, sql_command, args=[]):
        cursor = self.connection.cursor()
        cursor.execute(sql_command, args)
        result = cursor.fetchall()
        cursor.close()
        return result

    @staticmethod
    def close():
        Dao.connection.close()
        Dao.connection = None


# if __name__ == '__main__':
#     dao = Dao()
#     items = dao.search('Ane')
#
#     print(items)
