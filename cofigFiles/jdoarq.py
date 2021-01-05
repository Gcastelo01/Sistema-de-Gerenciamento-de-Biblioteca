import PySimpleGUI as sg
import functions.libFunctions as func
import functions.Json_Processor as jp
import shutil
import mysql.connector.errors
import _tkinter

img_dir = jp.img_retrivre()


def tela_de_cadastro():
    """Função responsável por gerar a tela de cadastro de um novo usuário, mostrar os termos de uso da aplicação,
    além de garantir que o usuário concorda com os termos de uso."""

    termos_de_uso = [[sg.Multiline('>>>>> LEIA ATENTAMENTE ANTES DE PROCEDER <<<<<\n'
                                   ''
                                   ' Termos de uso: A senha deve ter no mínimo 8 caracteres.'
                                   'qualquer coisa menor será desconsiderada. O sistema reconhece '
                                   'maiúsculas e minúsculas. Todos os direitos do código fonte deste prrograma são'
                                   ' reservados ao seu criador. Qualquer tentativa de copiar ou imitar deve ser '
                                   'devidamente autorizada pelo criador.',
                                   enter_submits=False, disabled=True, size=(60, 6))],
                     [sg.Text('', size=(40, 1), text_color='red', key='aviso')],
                     [sg.Checkbox('Eu li e concordo com os termos de uso', key='ok'), sg.Button('OK')]]
    window2 = sg.Window('Tela de Cadastro', termos_de_uso)

    while True:

        event2, values2 = window2.read()

        if event2 is None:
            '''Caso o usuário clique em cancelar ou no X, a janela irá se fechar encerrar a execução desse trecho de 
            código.'''

            window2.close()
            break

        if event2 == 'OK':

            """Caso o usuário clique em ok, o programa verifica se o usuário concordou com os termos de uso. Caso ele não
            tenha concordado, o programa exibe uma mensagem de que concordar com os termos são necessários."""

            if values2['ok'] is not True:
                window2['aviso'].update('É necessário concordar com os termos de uso.')
                window2['aviso']('É necessário concordar com os termos de uso.')

            else:
                window2.close()
                novo_cad = [[sg.Text('Nome de usuário: '), sg.InputText(key='newuser')],
                            [sg.Text('Senha: '), sg.InputText(password_char='*', key='pass')],
                            [sg.Text('Confirme sua senha: '), sg.InputText(password_char='*', key='confpass')],
                            [sg.Text('', size=(40, 1), text_color='red', justification='center', key='aviso')],
                            [sg.Button('Confirmar', key='conf'), sg.Button('Cancelar')]]
                tela_novocad = sg.Window('Tela de Cadastro', novo_cad, element_justification='right')
                while True:
                    event3, values3 = tela_novocad.read()

                    if event3 is None:
                        tela_novocad.close()
                        break

                    if event3 == 'conf':
                        if values3['pass'] == values3['confpass'] and len(values3['pass']) >= 8:  # Verifica se a senha
                            if func.cadastro_db(values3['newuser'],
                                                values3['pass']):  # Está dentro dos valores estipulados.
                                sg.PopupOK('Novo usuário Registrado!')
                                tela_novocad.close()
                                break
                            else:

                                tela_novocad['aviso'].update('Nome de usuário já cadastrado.')
                                tela_novocad['aviso']('Nome de usuário já cadastrado.')

                        elif len(values3['pass']) < 8:
                            tela_novocad['aviso'].update('A senha deve ter no Mínimo 8 caracteres.')
                            tela_novocad['aviso']('A senha deve ter no Mínimo 8 caracteres.')
                        elif values3['pass'] != values3['confpass']:
                            tela_novocad['aviso'].update('As senhas não coincidem')
                            tela_novocad['aviso']('As Senhas não coincidem.')
                    if event3 == 'Cancelar':
                        tela_novocad.close()
                        break
                break


def tela_de_login():
    """Tela de login da aplicação. Conectada com BD para poder verificar se o usuário digitou corretamente"""

    layout = [[sg.Image(img_dir + '\Background.png',
                        key='img')],
              [sg.Text('TELA DE LOGIN', justification='center', size=(45, 1), font='rockwell')],
              [sg.Text('Login: ', size=(8, 1), justification='left'), sg.Input(key='login')],
              [sg.Text('Senha: ', size=(8, 1), justification='left'), sg.Input(key='senha', password_char='*')],
              [sg.Button('Login', button_color=('darkblue', 'orange'), key='1'),
               sg.Button('Sing up', button_color=('black', 'lightblue'), key='2')]]

    window = sg.Window('Biblioteca Online', element_justification='center', layout=layout)

    while True:

        event, values = window.read()
        if event is None:
            window.close()
            return None
        if event == '1':
            if func.logsis(values['login'], values['senha']):
                window.Close()
                return True
            else:
                sg.PopupError('Login ou senha Incorretos!')
        if event == '2':
            tela_de_cadastro()


def tela_de_menu():
    """Menu principal da aplicação. Ele é responsável por retornar as escolhas do usuário"""

    sg.ChangeLookAndFeel('SystemDefault')
    layout = [[sg.Column([[sg.Button('Cadastro de novo livro', key='1', size=(30, 1))],
                          [sg.Button('Consultar tabela de Livros', key='2', size=(30, 1))],
                          [sg.Button('Menu de Empréstimos', key='3', size=(30, 1))],
                          [sg.Text('\n \n \n \n \n \n \n \n \n')],
                          [sg.Button('Fechar', key='6', size=(15, 1), button_color=('white', 'red'))]]), sg.Image(
        img_dir + '\Background.png')]]
    window = sg.Window('Biblioteca Online', layout, element_justification='right', size=(600, 400),
                       grab_anywhere=False)

    while True:
        event, values = window.Read()

        if event in (None, '6'):
            window.close()
            return 6
        if event == '1':
            return 1
        if event == '2':
            return 2
        if event == '3':
            return 3


def menu_de_nlivros():

    """Menu onde novos livros são cadastrados, inserindo as informações principais acerca do livro em questão,
    além de uma imagem da capa"""

    layout_da_coluna = [[sg.Text('Título: '), sg.InputText(key='0', size=(30, 1))],
                        [sg.Text('Autor: '), sg.InputText(key='1', size=(30, 1))],
                        [sg.Text('Editora: '), sg.InputText(key='2', size=(30, 1))],
                        [sg.Text('Ano de Publicação: '), sg.InputText(key='3', size=(30, 1))],
                        [sg.Text('Edição: '), sg.InputText(key='4', size=(30, 1))],
                        [sg.Text('Idioma: '), sg.InputText(key='5', size=(30, 1))],
                        [sg.Text('Ano de compra: '), sg.InputText(key='6', size=(30, 1))],
                        [sg.Text('Volume (se houver): '), sg.InputText(key='7', size=(30, 1))],
                        [sg.Text('Preço de compra: R$'), sg.InputText(key='8', size=(30, 1))],
                        [sg.Text('Nº de Páginas: '), sg.InputText(key='9', size=(30, 1))],
                        [sg.Text('Estado de Conservação: '), sg.Combo(('Muito Bom', 'Bom',
                                                                       'Regular', 'Ruim', 'Muito Ruim'), size=(28, 1),
                                                                      key='10', readonly=True)],
                        [sg.Text('Por favor, complete todos os campos corretamente!', visible=False, text_color='red',
                                 key='alerta')]]

    layout_da_coluna2 = [[sg.Text('Selecione o arquivo da imagem do livro '
                                  '(somente arquivos .PNG):')], [sg.InputText(key='11', enable_events=True),
                                                                 sg.FileBrowse('Pesquisa...')],
                         [sg.Image(key='imagem')]
                         ]

    layout = [[sg.Column(layout_da_coluna, element_justification='right'),
               sg.VerticalSeparator(), sg.Column(layout_da_coluna2, element_justification='right')],
              [sg.Button('Confirmar', button_color=('white', 'green'), key='conf'), sg.Button('Cancelar',
                                                                                              button_color=(
                                                                                                  'white', 'red'))]]

    window = sg.Window('Cadastro de livro', layout, element_justification='center', location=(330, 150),
                       no_titlebar=True)

    while True:
        event, values = window.Read()

        try:
            window['imagem'].update(filename=values['11'])

        except _tkinter.TclError:

            sg.PopupOK('A imagem deve estar no formato .PNG!', title='Erro')
            window['11'].Update(value='')

        if event in (None, 'Cancelar'):
            window.close()
            break

        if event == 'conf':

            filename = str(values['11'])
            im = filename.split('/')
            img_path = img_dir + '\\' + im[-1]

            try:
                shutil.move(values['11'], img_dir)

            except shutil.Error:
                ''
            try:

                func.cadastro_de_livro(values['0'], values['1'], values['2'], values['3'], values['4'], values['5'],
                                       values['6'], values['7'], values['8'], values['9'], values['10'], img_path)
                window.close()
                break

            except mysql.connector.errors.ProgrammingError:

                window['alerta'].update(visible=True)


def busca_de_livro():
    """Função responsável por mostrar a tela principal de buscas dentro dos livros cadastrados na biblioteca"""

    layout_da_coluna = [
        [sg.Text('Título: '), sg.Text(key=0, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Autor: '), sg.Text(key=1, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Editora: '), sg.Text(key=2, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Ano de Publicação: '),
         sg.Text('', key=3, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Edição: '), sg.Text(key=4, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Idioma: '), sg.Text(key=5, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Ano de compra: '), sg.Text(key=6, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Volume (se houver): '),
         sg.Text(key=7, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Preço de compra: R$'),
         sg.Text(key=8, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Nº de Páginas: '), sg.Text(key=9, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Estado de Conservação: '),
         sg.Text(key=10, size=(30, 1), background_color='darkblue', text_color='yellow')],
        [sg.Text('Status de empréstimo: '),
         sg.Text(key=11, size=(30, 1), background_color='darkblue', text_color='yellow')]]

    layout_da_coluna2 = [[sg.Text('Imagem da capa:')],
                         [sg.Image('', key='imagem')]]

    layout = [[sg.Text('Digite o Título')],
              [sg.InputText(key='livro'),
               sg.Button(key='pesq',
                         image_filename=img_dir + '\Imagem1.png', image_size=(20, 20),
                         image_subsample=3, button_color=('white', 'white'), size=(20, 20))],
              [sg.Column(layout_da_coluna, element_justification='right'), sg.VerticalSeparator(),
               sg.Column(layout_da_coluna2, element_justification='right')],
              [sg.Button('Sair', button_color=('white', 'darkred'), key='sair')]]

    window = sg.Window('Pequisa', layout, element_justification='center', location=(360, 100))

    while True:

        events, values = window.Read()

        if events in (None, 'sair'):

            window.close()
            break

        if events == 'pesq':

            resultado = func.pesquisa_no_bd(values['livro'])

            if len(resultado) == 0:

                sg.ChangeLookAndFeel('Material1')
                sg.PopupOK('Não existem Livros registrados com esse título! ', no_titlebar=False)
                sg.ChangeLookAndFeel('SystemDefault')

            else:
                for x in range(0, 12):

                    window[x].update(resultado[0][x])
                window['imagem'].update(resultado[0][12])


def menu_de_empréstimos():
    sg.ChangeLookAndFeel('Reddit')
    layout_da_coluna = [[sg.Button('Emprestar um livro', key='1', size=(20, 1))],
                        [sg.Button('Livros emprestados', key='2', size=(20, 1))],
                        [sg.Button('Receber Livro', key='3', size=(20, 1))],
                        [sg.Text('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')],
                        [sg.Button('Fechar', key='4', button_color=('white', 'red'), size=(20, 1))]]

    layout = [[sg.Image(img_dir + '\Julius.png'),
               sg.Frame('', layout_da_coluna, key='col', element_justification='right')]]
    window = sg.Window('Empréstimo', layout)

    while True:
        events, values = window.Read()

        if events in (None, '4'):
            window.Close()

            break
        elif events == '1':
            func.emprestar_um_livro()
        elif events == '2':
            func.emprestados()
        elif events == '3':
            func.recebimento()
