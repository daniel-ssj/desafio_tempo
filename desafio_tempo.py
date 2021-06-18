import requests
import zipfile
from io import BytesIO
import re
import pandas

def download(url, file_name=''):
    try:
        with requests.get(url) as req:
            if not file_name:
                file_name = file_name = req.url[url.rfind('/')+1:] + '.zip'

            with open(file_name, 'wb') as file:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            return file_name
    
    except Exception as e:
        print('There was a problem when attempting to download the file:\n{}', e)
        return None

def custo_marginal(file_name):
    try:
        with zipfile.ZipFile(file_name, 'r') as zip:
            for name in zip.namelist():
                if name == 'Relatorio_Sumario-202106-sem1.zip':
                    relatoriozip = BytesIO(zip.read(name))
                    with zipfile.ZipFile(relatoriozip) as relatorio:
                        #converte o relatorio de bytes para string com o metodo decode()
                        string = relatorio.read('relato.rv0').decode('utf-8', 'ignore')

                        #pega a parte do relatorio que mostra o custo marginal de cada subsistema
                        string = string[string.find('Custo marginal de operacao do subsistema'):string.rfind('239.61 ($/MWh)')+14]

                        #extrai os numeros dessa parte do relatorio
                        numbers = re.findall('\d+\.\d+', string)

                        #cria um dicionario com o nome dos subsistemas e custo marginal
                        data = {'subsistema': ['SE', 'S', 'NE', 'N', 'FC'], 'custo marginal': numbers}

                        #transforma dicionario em dataframe com pandas
                        df = pandas.DataFrame(data=data)

                        #imprime dataframe na tela
                        print(df)
                        
    except Exception as e:
        print(f'There was a problem trying to read the file:\n{e}')


file_name = download('https://www.ccee.org.br/ccee/documentos/DC202106')
custo_marginal(file_name)
