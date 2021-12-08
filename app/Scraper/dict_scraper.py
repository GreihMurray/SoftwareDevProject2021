import unicodedata
import regex
import requests
from bs4 import BeautifulSoup
import json
import PyPDF2

clean_words = {}

start_chars = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'NG', 'H', 'I', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']

for char in start_chars:
    print('Starting on ', char)
    URL = 'http://www.dil.ie/browse/' + char
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a', class_='browse_show')

    for link in links:
        if link.contents:
            bits = link.contents[0].split('<')
            pieces = bits[0].split('>')
            word = str(unicodedata.normalize('NFC', pieces[0])).lower()

            word = regex.sub(r'([^\p{L}\'])', '', word)

            if word not in clean_words.keys():
                clean_words[word] = 1
        else:
            continue

pdfFile = open('gv2ga.pdf', 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFile)

for i in range(4, pdfReader.numPages):
    pages = pdfReader.getPage(i)
    print('Page ', (i - 3), ' of ', (pdfReader.numPages - 3))
    words = pages.extractText().split('\n')

    for word in words:
        clean = regex.sub(r'([^\p{L}\'\-])', '', word)
        if not clean or len(clean) <= 3:
            continue
        elif word not in clean_words.keys():
            clean_words[clean] = 1

pdfFile.close()

print(list(clean_words.keys()))

out = open('full_irish_dict.json', "a", encoding='utf-8')
json_db = json.dumps(list(clean_words.keys()), ensure_ascii=False)
out.write(json_db)
out.close()