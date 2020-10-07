# A Base do programa d
import mysql.connector as bd
import PySimpleGUI as sg
import funçoes.Json_Processor as jp

livros = list()
db_log = jp.db_log_retriver()
img_dir = jp.img_retrivre()

cnx = bd.connect(user=db_log['user'], password=db_log['password'], host=db_log['host'], auth_plugin=db_log['auth_plugin'])
user = cnx.cursor()

user.execute('USE APP_BIBLIOTECA')
user.execute('select * from login')
login_sistema = user.fetchall()


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


def cadastro_de_livro(title, aut, edt, anp: int, edi, idi, ac: int, vol: int, rs, numpag: int, edc, img: str):

    """Ligação com o banco de dados, enviando os dados do novo livro recém cadastrado dentro da tela de cadastro"""

    user.execute(f"INSERT INTO LIVROS VALUES('{title}', '{aut}', '{edt}', {anp}, {edi}, '{idi}', {ac}, {vol}, {rs}, "
                 f"{numpag}, '{edc}', 'E','{img}')")
    cnx.commit()


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


def emprestados():

    """"""

    user.execute('SELECT NOME_DO_LIVRO FROM EMPRESTADOS')
    empres = user.fetchall()
    if len(empres) == 0:
        sg.PopupOK('Não há livros emprestados!')
    else:
        layout = [[sg.Text('Selecione o Titulo emprestado do qual deseja \n'
                           'ver informações: ', font=('timesnewroman', 10))],
                  [sg.Text('', key='al', text_color='darkred', font=('timesnewroman', 10), size=(40, 1))],
                  [sg.Combo(empres, readonly=True, size=(50, 1), key='n'), sg.Button('Confirma', key='c')]]

        window = sg.Window('Livros emprestados', layout)
        while True:
            events, values = window.Read()
            if events is None:
                window.Close()
                break
            if values['n'] == '':
                window['al'].Update('Nenhum Livro selecionado!')
                window['al']('Nenhum Livro selecionado!')
            elif events == 'c':
                user.execute(f"SELECT * FROM EMPRESTADOS WHERE NOME_DO_LIVRO = '{values['n'][0]}'")
                intel = user.fetchall()
                layout2 = [[sg.Text('Com quem Está: '),
                            sg.Text(f'{intel[0][0]}', size=(30, 1), background_color='darkblue',
                                    text_color='yellow')],

                           [sg.Text('Nome do Livro: '),
                            sg.Text(f'{intel[0][1]}', size=(30, 1), background_color='darkblue',
                                    text_color='yellow')],

                           [sg.Text('Código do Livro: '),
                            sg.Text(F'{intel[0][2]}', size=(30, 1), background_color='darkblue',
                                    text_color='yellow')],

                           [sg.Text('Data de Empréstimo: '),
                            sg.Text(f'{intel[0][3][:2]}/{intel[0][3][2:4]}/{intel[0][3][4:]}',
                                    size=(30, 1), background_color='darkblue',
                                    text_color='yellow')],

                           [sg.Text('Data de Devolução: '),
                            sg.Text(f'{intel[0][4][0:2]}/{intel[0][4][2:4]}/{intel[0][4][4:]}',
                                    size=(30, 1), background_color='darkblue',
                                    text_color='yellow')],

                           [sg.Button('OK', key='o', button_color=('white', 'green'))]]

                window2 = sg.Window(f'{intel[0][1]}', layout2, element_justification='right')
                events2, values2 = window2.Read()
                if events2 in (None, 'o'):
                    window2.Close()
                    break


def emprestar_um_livro():

    """Tela responsável por fazer o empréstimo dos livros"""

    layout = [[sg.Text('Nome do Livro: '), sg.InputText(key='title')],
              [sg.Text('Quem está Recebendo: '), sg.InputText(key='receptor')],
              [sg.Text('Data de empréstimo: '), sg.InputText(key='dataemp')],
              [sg.Text('Data de devolução: '), sg.InputText(key='datadev')],
              [sg.Button('Confirmar', key='conf'), sg.Button('Cancelar', key='cancel')]]

    window = sg.Window('Empréstimo', layout, text_justification='left', element_justification='right')

    código = 00000
    user.execute('SELECT TÍTULO FROM LIVROS')
    meus_lvros = user.fetchall()

    while True:
        event, values = window.Read()
        print(values['title'])
        user.execute(f"SELECT STATUS_DO_LIVRO FROM LIVROS WHERE TÍTULO = '{values['title']}'")
        check = user.fetchall()
        if event in (None, 'cancel'):
            window.Close()
            break
        if event == 'conf':
            if check[0][0] == 'E':
                sg.PopupOK('Título já se encontra emprestado!')
            elif values['title'] in meus_lvros[0]:
                if values['title'] != '' and values['receptor'] != '' and values['dataemp'] != '':
                    data = str(values['dataemp']).replace('/', '')
                    datadev = (str(values['datadev']).replace('/', ''))
                    user.execute(f"INSERT INTO EMPRESTADOS VALUES('{values['receptor']}', '{values['title']}', {código},"
                                 f"{data}, {datadev})")
                    user.execute(F"UPDATE LIVROS SET STATUS_DO_LIVRO = 'E' WHERE TÍTULO = '{values['title']}'")
                    cnx.commit()
                    sg.PopupOK('Livro emprestado!')
                    window.Close()
                    break
                else:
                    sg.PopupOK('Favor preencher todos os campos!')
            else:
                sg.PopupOK('O livro em questão não está registrado.')


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
