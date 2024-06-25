from ast import Set
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

# Criando a engine do SQLAlchemy que se conecta a um banco de dados SQLite chamado "results.db"
engine = sqlalchemy.create_engine("sqlite:///results.db")
# Criando uma classe base para a definição das classes de mapeamento ORM
Base = declarative_base()
# Criando uma classe Session configurada para ser ligada à engine
Session = sessionmaker(bind=engine)
# Criando uma instância de sessão para interagir com o banco de dados
session = Session()


# Classe mapeada que representa uma tabela no banco de dados
class Result(Base):
    # Nome da tabela no banco de dados.
    __tablename__ = "results"
    # Colunas da tabela com seus respectivos tipos e propriedades.
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    logradouro = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(50))
    estado = Column(String(20))
    cep = Column(String(20))
    telefone = Column(String(20))
    website = Column(String(150))

    def __repr__(self):
        return f"<Endereco(id={self.id}, nome='{self.nome}', logradouro='{self.logradouro}', bairro='{self.bairro}', cidade='{self.cidade}', estado='{self.estado}', cep='{self.cep}', telefone='{self.telefone}', website='{self.website}')>"


def inserir_dados(lista):
    # Inserir a lista com dados no banco de dados.
    if not lista:
        print("Nada a processar!")
    else:

        try:
            session.add_all(lista)
            session.commit()
            print("Dados inseridos com sucesso!")
        except Exception as e:
            print(f"Erro! {e}")


def inicializar_bd():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Erro! {e}")
