# A Base do programa 
import mysql.connector as bd
import PySimpleGUI as sg
import Json_Processor as jp

db_log = jp.db_log_retriver()
img_dir = jp.img_retrivre()

#TODO: Fazer a função de recuperação dos múltiplos usuários, permitindo que ele escolha qual livro deseja ver.



class __DatabaseSetup__():
    def __init__(self):
        self.__cnx = bd.connect(user=db_log['user'], password=db_log['password'], host=db_log['host'], auth_plugin=db_log['auth_plugin'])
        self.__user = self.__cnx.cursor()


    def __databaseCheck(self, username):

        self.__user.execute('SELECT * FROM login')
        return self.__user.fetchall()



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



class Livro():
    def __init__(self):
        self.cnx = bd.connect(user=db_log['user'], password=db_log['password'], host=db_log['host'], auth_plugin=db_log['auth_plugin'])
        self.user = self.cnx.cursor()

    def cadastro_de_livro(self, title, aut, edt, anp: int, edi, idi, ac: int, vol: int, rs, numpag: int, edc, img: str):

        """Ligação com o banco de dados, enviando os dados do novo livro recém cadastrado dentro da tela de cadastro"""

        self.user.execute(f"INSERT INTO LIVROS VALUES('{title}', '{aut}', '{edt}', {anp}, {edi}, '{idi}', {ac}, {vol}, {rs}, "
                    f"{numpag}, '{edc}', 'E','{img}')")
        self.cnx.commit()


    def estado(self, titulo):
        
        self.user.execute(f"SELECT * FROM EMPRESTADOS WHERE TÍTULO LIKE %{titulo}%;")
        __result = self.user.fetchall()

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

                    self.user.execute(f"INSERT INTO EMPRESTADOS VALUES('{nome_do_credor}', '{titulo}', {codigo},"
                                 f"{data}, {datadev})")

                    self.user.execute(F"UPDATE LIVROS SET STATUS_DO_LIVRO = 'E' WHERE TÍTULO = '{titulo}'")
                    self.cnx.commit()

    def receber(self, titulo):
        try:
            __estado = self.estado(titulo)

        except titulo == '':
            "Popup de 'Por favor insira um título'"

        if __estado == 'E':

            self.user.execute(f"UPDATE LIVROS SET STATUS_DO_LIVRO = 'NE' WHERE TÍTULO = '{titulo}'")
            self.cnx.commit()
            self.user.execute(f"DELETE FROM EMPRESTADOS WHERE NOME_DO_LIVRO = '{titulo}'")
            self.cnx.commit()

    def procurarDB(self, titulo):
        """Essa função é responsável por buscar dentro do banco de dados as informações referentes ao título do livro que
        foi pesquisa"""

        self.user.execute(f"SELECT TÍTULO FROM LIVROS WHERE TÍTULO LIKE '%{titulo}%'")
        tanto = self.user.fetchall()

        if len(tanto) > 1:
            esc = self.multiplos_resultados(tanto)
            self.user.execute(f"SELECT * FROM LIVROS WHERE TÍTULO = '{esc}'")
            resultado = self.user.fetchall()
            return resultado

        else:
            self.user.execute(f"SELECT * FROM LIVROS WHERE TÍTULO LIKE '%{titulo}%'")
            resultado = self.user.fetchall()
            return resultado


    def multiplos_resultados(self, results: list):
        # Aqui vai entrar a lógica por trás da seleção de multiplos resultados
        return results[0] 
