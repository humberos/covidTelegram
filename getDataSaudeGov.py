import requests
import json
import csv

url = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalMapa"

payload = {}
headers = {
  'authority': 'xx9p7hp1p7.execute-api.us-east-1.amazonaws.com',
  'method': 'GET',
  'path': '/prod/PortalMapa',
  'scheme': 'https',
  'accept': 'application/json, text/plain, */*',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'en-US,en;q=0.9,pt;q=0.8',
  'dnt': '1',
  'origin': 'https://covid.saude.gov.br',
  'referer': 'https://covid.saude.gov.br/',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4100.3 Safari/537.36',
  'x-parse-application-id': 'unAFkcaNDeXajurGB7LChj8SgQYS2ptm'
}

response = requests.request("GET", url, headers=headers, data = payload)

dadosGov = json.loads(response.text.encode('utf8'))

# print(dadosGov['results'][0])


outputFile = open('data/brazil_states.csv', 'w')  # load csv file

output = csv.writer(outputFile)  # create a csv.write
del dadosGov['results'][0]['percent']
output.writerow(dadosGov['results'][0].keys())  # header row
# print(dadosGov['results'][2].values())
# exit()
states = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

for x in states:
  for dados in dadosGov['results']:    
    if dados['nome'] == states[x]:
      dados['nome'] = (x)

for row in dadosGov['results']:      
  output.writerow(row.values())

