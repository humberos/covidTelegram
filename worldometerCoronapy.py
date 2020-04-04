
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import date

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

today = date.today()



def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = session.get(url)
    # return the soup
    return bs(html.content, "html.parser")


def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers


def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows


def save_as_csv(table_name, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")



url = 'https://www.worldometers.info/coronavirus/'

# soup = BeautifulSoup(data.content, 'html.parser')

soup = get_soup(url)
tables = soup.find_all("table")
# print(f"[+] Found a total of {len(tables)} tables.")
# iterate over all tables
# for i, table in enumerate(tables, start=1):
# get the table headers
headersToday = get_table_headers(tables[0])
headersYesterday = get_table_headers(tables[1])
# get all the rows of the table
rowsToday = get_table_rows(tables[0])
rowsYesterday = get_table_rows(tables[1])
# save table as csv file
tableToday = "today"
tableYesterday = (str(today.day)+"_"+str(today.month)+"_" + str(today.year))
# print(f"[+] Saving {table_name}")
save_as_csv(tableToday, headersToday, rowsToday)
save_as_csv(tableYesterday, headersYesterday, rowsYesterday)
print('Updated!')
# tbl = soup.find("table", {"id": "main_table_countries_today"})

# data_frame = pd.read_html(str(tbl))


# print data_frame.to_csv(index=False)
