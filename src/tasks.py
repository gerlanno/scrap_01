from model import Result


def separar_endereco(endereco_completo):
    # Dividir pelo delimitador de país
    partes = endereco_completo.rsplit(",", 1)
    endereco_sem_pais = partes[0].strip()
    pais = partes[1].strip()

    # Dividir pelo delimitador de CEP
    partes = endereco_sem_pais.rsplit(",", 1)
    endereco_sem_cep = partes[0].strip()
    cep = partes[1].strip()

    # Dividir pelo delimitador de estado (última ocorrência de "-")
    partes = endereco_sem_cep.rsplit("-", 1)
    endereco_sem_cidade = partes[0].strip()
    estado = partes[1].strip()

    # Dividir pelo delimitador de cidade (última vírgula)
    partes = endereco_sem_cidade.rsplit(",", 1)
    endereco_bairro = partes[0].strip()
    cidade = partes[1].strip()

    # Dividir pelo delimitador de número e bairro
    partes = endereco_bairro.split(" - ", 1)
    logradouro = partes[0].strip()
    bairro = partes[1].strip() if len(partes) > 1 else ""

    return {
        "logradouro": logradouro,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "cep": cep,
        "pais": pais,
    }


def processar_dados(dict_pesquisa):
    """
    Processamento dos dados recebidos da API
    """

    lista_resultados = []
    for resultado in dict_pesquisa["local_results"]:
        nome = resultado.get("title")
        if not resultado.get("address") == None:
            # Função para separar o endereço que vem completo em uma só string em cada variavel respectiva.
            endereco = separar_endereco(resultado.get("address"))
            logradouro = endereco.get("logradouro")
            bairro = endereco.get("bairro")
            cep = endereco.get("cep")
            cidade = endereco.get("cidade")
            estado = endereco.get("estado")
        else:
            logradouro = ""
            bairro = ""
            cep = ""
            cidade = ""
            estado = ""
        telefone = (
            resultado.get("phone").replace("+", "").replace("-", "").replace(" ", "")# Retirar espaços e caracteres especiais dos números de telefone
            if resultado.get("phone")
            else ""
        )
        website = resultado.get("website")
        lista_resultados.append(
            Result(
                nome=nome,
                logradouro=logradouro,
                bairro=bairro,
                cep=cep,
                cidade=cidade,
                estado=estado,
                telefone=telefone,
                website=website,
            )
        )
    return lista_resultados
