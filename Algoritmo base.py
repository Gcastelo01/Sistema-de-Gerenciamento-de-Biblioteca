# A Base do programa da biblioteca
import cofigFiles.jdoarq as ps

while True:

    '''Trecho do código responsável por gerenciar o login do usuário. caso o deu não seja true, o usuário fica preso
    em um loop até que acerte a senha ou desista de tentar e feche o programa'''

    deu = ps.tela_de_login()

    if deu is None:
        break
    elif deu:
        deu = 'blz'
        break

while deu == 'blz':

    menu_de_opções = ps.tela_de_menu()
    '''Aqui é a lógica de funcionamento principal do programa. De acordo com a seleção do usuário,
    o programa se encaminha para uma outra tela, de acordo com a seleção'''

    if menu_de_opções == 1:
        ps.menu_de_nlivros()
    elif menu_de_opções == 2:
        ps.busca_de_livro()
    elif menu_de_opções == 3:
        ps.menu_de_empréstimos()
    elif menu_de_opções == 6:
        break
