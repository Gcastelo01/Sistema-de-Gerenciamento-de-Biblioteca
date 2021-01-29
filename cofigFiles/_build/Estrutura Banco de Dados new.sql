CREATE DATABASE APP_BIBLIOTECA;
USE APP_BIBLIOTECA;

CREATE TABLE LOGIN(
	USUÁRIO VARCHAR(20),
	SENHA VARCHAR(20)
);

INSERT INTO LOGIN(USUÁRIO, SENHA) VALUES('root', 'toor');

//

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

	
ALTER TABLE LIVROS MODIFY COLUMN STATUS_DO_LIVRO CHAR(2) DEFAULT 'NE';

SELECT STATUS_DO_LIVRO, COUNT(*) FROM livros 
GROUP BY STATUS_DO_LIVRO;  /*Aqui contamos os livros na tabela, agrupando todos os registros de acordo com seus estados, ou seja, 
                            eles vão ser sorteados entre dois tipos: E e NE. Desse modo, podemos separar por categorias*/

//

