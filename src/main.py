import sys
import os
import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import settings
from serpapi import GoogleSearch
from data import processar_dados
from model import inserir_dados, inicializar_bd


def google_maps(query):
    # Criar a tabela, caso nao exista, de acordo com a classe mapeada.
    inicializar_bd()

    query = query

    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "hl": "pt-br",
        "api_key": settings.API_KEY,
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        # Tratando os dados antes de inseri-los no banco.
        inserir_dados((processar_dados(results)))
    except Exception as e:
        print(f"Erro: {e}")


try:
    operacao = sys.argv[1].lower()

    if operacao == "maps":

        query = sys.argv[2]
        google_maps(query)
    else:
        print("Erro!")
except Exception as e:
    print(f"erro: {e}")
