import sys
import os
import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import settings
from serpapi import GoogleSearch
from data import processar_dados
from model import inserir_dados, inicializar_bd
from urllib.parse import parse_qsl, urlsplit


def google_maps(query):
    # Criar a tabela, caso nao exista, de acordo com a classe mapeada.
    inicializar_bd()

    query = query
    # Parametros
    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "hl": "pt-br",
        "ll": "@-3.775399,-38.521686,25.5z",
        "api_key": settings.API_KEY,
    }
    search = GoogleSearch(params)  # Obter dados da pesquisa
    try:
        while True:

            results = search.get_dict()

            if "error" in results:
                print(results["error"])
                break
            # Tratar e inserir os resultados da página atual no banco de dadaos.
            inserir_dados((processar_dados(results)))
            # Verificar se existe uma próxima página nos resultados e fazer a chamada.
            if "next" in results.get("serpapi_pagination", {}):
                # Separando a query da url e gerando um conjunto de chaves:valor que serão inseridos nos parametros.
                search.params_dict.update(
                    dict(
                        parse_qsl(
                            urlsplit(
                                results.get("serpapi_pagination", {}).get("next")
                            ).query
                        )
                    )
                )
            else:
                break

    except Exception as e:
        print(f"Erro: {e}")


try:
    # Parametros para a chamada do script: 1 - engine ("maps") 2 - query("pesquisa local")
    operacao = sys.argv[1].lower()

    if operacao == "maps":

        query = sys.argv[2]
        google_maps(query)
    else:
        print("Erro!")
except Exception as e:
    print(f"erro: {e}")
