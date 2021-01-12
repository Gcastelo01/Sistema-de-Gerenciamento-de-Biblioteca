# A Base do programa d
import mysql.connector as bd
import PySimpleGUI as sg
import Json_Processor as jp

livros = list()
db_log = jp.db_log_retriver()
img_dir = jp.img_retrivre()

cnx = bd.connect(user=db_log['user'], password=db_log['password'], host=db_log['host'], auth_plugin=db_log['auth_plugin'])
user = cnx.cursor()

user.execute('USE APP_BIBLIOTECA')
user.execute('select * from login')
login_sistema = user.fetchall()



class Livro():
    
    def cadastro_de_livro(self, title, aut, edt, anp: int, edi, idi, ac: int, vol: int, rs, numpag: int, edc, img: str):

        """Ligação com o banco de dados, enviando os dados do novo livro recém cadastrado dentro da tela de cadastro"""

        user.execute(f"INSERT INTO LIVROS VALUES('{title}', '{aut}', '{edt}', {anp}, {edi}, '{idi}', {ac}, {vol}, {rs}, "
                    f"{numpag}, '{edc}', 'E','{img}')")
        cnx.commit()


    def estado(self, titulo):
        
        user.execute(f"SELECT * FROM EMPRESTADOS WHERE TÍTULO LIKE %{titulo}%;")
        __result = user.fetchall()

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

                    user.execute(f"INSERT INTO EMPRESTADOS VALUES('{nome_do_credor}', '{titulo}', {codigo},"
                                 f"{data}, {datadev})")

                    user.execute(F"UPDATE LIVROS SET STATUS_DO_LIVRO = 'E' WHERE TÍTULO = '{titulo}'")
                    cnx.commit()

    def receber(self, titulo):
        try:
            __estado = self.estado(titulo)

        except titulo == '':
            "Popup de 'Por favor insira um título'"

        if estado == 'E':
            return False
        else:
            if nome_do_credor != '' and data_de_emprestimo != '':
                    data = str(data_de_emprestimo).replace('/', '')
                    datadev = (str(data_de_dev).replace('/', ''))

                    user.execute(f"INSERT INTO EMPRESTADOS VALUES('{nome_do_credor}', '{titulo}', {codigo},"
                                 f"{data}, {datadev})")

                    user.execute(F"UPDATE LIVROS SET STATUS_DO_LIVRO = 'E' WHERE TÍTULO = '{titulo}'")
                    cnx.commit()





def logsis(log, sen):

    """Responsável por verificar se o usuário digitou um usuário válido e sua senha correspondente"""

    for v in login_sistema:
        if v[0] == log and v[1] == sen:
            return True
    else:
        return False


def cadastro_db(log, sen):

    """Insere dados de um novo usuário caso ele não exista nos registros do banco de dados """
    
    for v in login_sistema:
        if v[0] == log:
            return False
    else:
        user.execute(f"INSERT INTO LOGIN (USUÁRIO, SENHA) VALUES('{log}', '{sen}')")
        cnx.commit()
        return True



def multiplos_resultados(results: list):

    """Quando uma pesquisa no banco de dados retorna múltiplos resultados de títulos de livros, seja a pesquisa de
    livros emprestados ou a lista total de livros cadastrada, esse popup permite ao usuário escolher qual dos títulos
    deseja visualizar"""

    layout = [[sg.Text('Multiplos resultdos encontrados. Selecione o que deseja vizualizar.')],
              [sg.Combo(results, key='0', size=(50, 1), readonly=True, font=['bahnschriftsemiLightsemiconde', 8])],
              [sg.Button('Ok', key='ok')]]

    window = sg.Window('Multiplos Resultados', layout)

    while True:
        events, values = window.read()

        if events is None:
            window.Close()
            break
        if events == 'ok':
            window.Close()
            return values['0'][0]


def pesquisa_no_bd(title):

    """Essa função é responsável por buscar dentro do banco de dados as informações referentes ao título do livro que
    foi pesquisa"""

    user.execute(f"SELECT TÍTULO FROM LIVROS WHERE TÍTULO LIKE '%{title}%'")
    tanto = user.fetchall()

    if len(tanto) > 1:
        esc = multiplos_resultados(tanto)
        user.execute(f"SELECT * FROM LIVROS WHERE TÍTULO = '{esc}'")
        resultado = user.fetchall()
        return resultado

    else:
        user.execute(f"SELECT * FROM LIVROS WHERE TÍTULO LIKE '%{title}%'")
        resultado = user.fetchall()
        return resultado


"""
def busca_de_tags(tag):

    Função para buscar livros na lista através de #
"""

def recebimento():

    """Função responsável por retirar da tabela de emprestados e devolver à tabela principal"""

    user.execute('SELECT NOME_DO_LIVRO FROM EMPRESTADOS')
    emprestado = user.fetchall()
    layout = [[sg.Text('Escolha o livro a ser recebido:')],
              [sg.Combo(emprestado, key='rec', readonly=True)],
              [sg.Button('Ok', key='ok'), sg.Button('Cancelar', key='can')]]

    window = sg.Window('Recebimento', layout)

    while True:
        event, values = window.Read()
        if event in (None, 'can'):
            window.Close()
            break
        elif event == 'ok':
            user.execute(f"UPDATE LIVROS SET STATUS_DO_LIVRO = 'NE' WHERE TÍTULO = '{values['rec'][0]}'")
            cnx.commit()
            user.execute(f"DELETE FROM EMPRESTADOS WHERE NOME_DO_LIVRO = '{values['rec'][0]}'")
            cnx.commit()
            sg.PopupOK('Livro devolvido à sua biblioteca!')
            window.Close()
            break
