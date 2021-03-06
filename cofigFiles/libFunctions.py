# A Base do programa
import mysql.connector as bd
import PySimpleGUI as sg
import os, sys, json



#TODO: Fazer a função de recuperação dos múltiplos resultados, permitindo que ele escolha qual livro deseja ver.

class __JsonSettings__():
    def __init__(self):
        self.db_log = self.__db_log_retriver__()

        self.__cnx = bd.connect(user=self.db_log['user'], password=self.db_log['password'], host=self.db_log['host'], auth_plugin=self.db_log['auth_plugin'])
        self.__user = self.__cnx.cursor()

    def __libInstaller__(self):
        path = os.path.abspath("../_build")
        write_path = path
        img_path = os.path.abspath('../icons')

        done = False
        if done is False:
            self.__user.execute("""CREATE DATABASE APP_BIBLIOTECA;
                                 USE APP_BIBLIOTECA;
                                 CREATE TABLE LOGIN(
                            	 USUÁRIO VARCHAR(20),
                            	 SENHA VARCHAR(20)
                                 );""")
            self.__user.execute("""
                                    CREATE TABLE LIVROS(
                                    	TÍTULO VARCHAR(100),
                                    	AUTOR VARCHAR(50),
                                    	EDITORA VARCHAR(50),
                                    	ANO_PUBLICAÇÃO INT(4),
                                    	EDIÇÃO INT(1),
                                    	IDIOMA VARCHAR(20),
                                    	ANO_COMPRA INT(4),
                                    	VOLUME INT(1),
                                    	PREÇO FLOAT(10.2),
                                    	PAGINAS INT(5),\A
                                    	STATUS_DO_LIVRO CHAR(2),
                                    	TAGS VARCHAR(150)
                                    );

                                    CREATE TABLE EMPRESTADOS(
                                    	NOME_DO_CREDOR VARCHAR(50),
                                    	NOME_DO_LIVRO VARCHAR(100),
                                    	CODIGO_DO_LIVRO INT(5),
                                    	DATA_DE_EMPRÉSTIMO INT(8),
                                    	DATA_DE_DEVOLUÇÃO INT(8)
                                    );
                        """)
                                 

            try:

                with open(os.path.join(path, 'UserAppInfo.json'), 'r') as f:
                    p_json = json.load(f)

                if p_json['install'] == '1':
                    done = True
                    return True

            except FileNotFoundError:

                path = os.path.join(path, 'DataBaseAccessDB.json')

                dados = {

                    'install': '1',
                    'DB_logger': path,
                    'Img_dir': img_path

                }
                with open(os.path.join(write_path, "UserAppInfo.json"), 'w') as file:
                    json.dump(dados, file, indent=4)


    def __path_invoke__(self):

        path = ".. .build"

        with open(os.path.join(path, 'UserAppInfo.json'), 'r') as f:
            return json.load(f)


    def __db_log_retriver__(self):
        self.__libInstaller__()
        log = self.__path_invoke__()

        with open(log['DB_logger'], 'r') as p_json:
            return json.load(p_json)






class __DatabaseSetup__(__JsonSettings__):
    def __init__(self):
        self.db_log = self.__db_log_retriver__()

        self.__cnx = bd.connect(user=self.db_log['user'], password=self.db_log['password'], host=self.db_log['host'], auth_plugin=self.db_log['auth_plugin'])
        self.__user = self.__cnx.cursor()


    def __databaseCheck(self, username):
        self.__libInstaller__()
        self.__user.execute('SELECT * FROM login')
        return self.__user.fetchall()

    def tagSearch(self, tag: tuple):

        self.__user.execute('SELECT TAGS, TÍTULOS FROM LIVROS')
        __tags = self.__user.fetchall()
        __taglist = list()
        __bookInTag = list()

        for V in __tags:
            __taglist = V[1].split(' ')

            for F in tag:
                if F in __taglist:
                    __bookInTag.append(V[0])

        return __bookInTag




class User(__DatabaseSetup__):

    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def cadastro_db(self):

        """Insere dados de um novo usuário caso ele não exista nos registros do banco de dados """

        for v in self.__databaseCheck(self.__username):
            if v[0] == self.__username:
                return False

        else:
            self.__user.execute(f"INSERT INTO LOGIN (USUÁRIO, SENHA) VALUES('{self.__username}', '{self.__password}')")
            self.__cnx.commit()
            return True

    def loginSist(self):

        for v in self.__databaseCheck(self.__username):
            if v[0] == self.__username and v[1] == self.__password:
                return True
        else:
            return False



class Livro(__DatabaseSetup__):
    def __init__(self):
        self.__taglist = tuple()

    def cadastro_de_livro(self, title, aut, edt, anp: int, edi, idi, ac: int, vol: int, rs, numpag: int, edc, img: str, tag: list):

        """Ligação com o banco de dados, enviando os dados do novo livro recém cadastrado dentro da tela de cadastro"""
        self.__taglist = str(tag)
        self.__taglist = ((((self.__taglist.replace(',', '')).replace('[', '')).replace(']', '')).replace("'", '')).lower()

        self.__user.execute(f"INSERT INTO LIVROS VALUES('{title}', '{aut}', '{edt}', {anp}, {edi}, '{idi}', {ac}, {vol}, {rs}, "
                    f"{numpag}, '{edc}', 'E','{img}', '{self.__taglist}')")
        self.__cnx.commit()


    def estado(self, titulo):

        self.__user.execute(f"SELECT * FROM EMPRESTADOS WHERE TÍTULO LIKE %{titulo}%;")
        __result = self.__user.fetchall()

        return __result


    def emprestar(self, titulo, codigo, nome_do_credor, data_de_emprestimo, data_de_dev):
        try:
            estado = self.estado(titulo)

        except titulo == '':
            "Popup de 'Por favor insira um título'"

        if estado == 'E':
            return False

        else:
            if nome_do_credor != '' and data_de_emprestimo != '':
                    data = str(data_de_emprestimo).replace('/', '')
                    datadev = (str(data_de_dev).replace('/', ''))

                    self.__user.execute(f"INSERT INTO EMPRESTADOS VALUES('{nome_do_credor}', '{titulo}', {codigo},"
                                 f"{data}, {datadev})")

                    self.__user.execute(F"UPDATE LIVROS SET STATUS_DO_LIVRO = 'E' WHERE TÍTULO = '{titulo}'")
                    self.__cnx.commit()

    def receber(self, titulo):
        try:
            __estado = self.estado(titulo)

        except titulo == '':
            "Popup de 'Por favor insira um título'"

        if __estado == 'E':

            self.__user.execute(f"UPDATE LIVROS SET STATUS_DO_LIVRO = 'NE' WHERE TÍTULO = '{titulo}'")
            self.__cnx.commit()
            self.__user.execute(f"DELETE FROM EMPRESTADOS WHERE NOME_DO_LIVRO = '{titulo}'")
            self.__cnx.commit()

    def procurarDB(self, titulo):
        """Essa função é responsável por buscar dentro do banco de dados as informações referentes ao título do livro que
        foi pesquisa"""

        self.__user.execute(f"SELECT TÍTULO FROM LIVROS WHERE TÍTULO LIKE '%{titulo}%'")
        tanto = self.__user.fetchall()

        if len(tanto) > 1:
            esc = self.multiplos_resultados(tanto)
            self.__user.execute(f"SELECT * FROM LIVROS WHERE TÍTULO = '{esc}'")
            resultado = self.__user.fetchall()
            return resultado

        else:
            self.__user.execute(f"SELECT * FROM LIVROS WHERE TÍTULO LIKE '%{titulo}%'")
            resultado = self.__user.fetchall()
            return resultado


    def multiplos_resultados(self, results: list):
        # Aqui vai entrar a lógica por trás da seleção de multiplos resultados
        return results[0]
