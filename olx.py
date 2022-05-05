import requests
import re


def ContainsDigit(inputString):
    for digit in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        if digit in inputString:
            return True
    return False
def ContainsOperator(inputString):
    for operator in ['~', '`', '!', '‼️',  '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '[', '}', ']', '|', '\\', ':', ';', '"', '\'', '<', ',', '>', '.', '?', '/']:
        if operator in inputString:
            return True
    return False
def InsertIntoRank(word, frequency):
    global maxes, words
    stack1 = []
    stack2 = []
    if len(maxes)<10 and frequency<maxes[len(maxes)-1]:
        maxes.append(frequency)
        words.append(word)
        return
    elif frequency>maxes[len(maxes)-1]:
        while frequency>maxes[len(maxes)-1]:
            stack1.append(maxes.pop())

url = "https://www.olx.ro/d/anunturi-agricole" #url-ul paginii de start
regex = re.compile('(?s)(?<=<h6 class=\"css-v3vynn-Text eu5v0x0\">).*?(?=</h6>)') #regex-ul pentru preluarea titlurilor
dict={} #dictionar pentru accesarea rapida a titlurilor si frecventelor ascoiate
maxes = [] #cele 10 cele mai mari frecvente
words = [] #cele 10 cele mai frecvente cuvinte
for i in range(1, 26): #25 de pagini max are OLX-ul
    print("page ",i) #improv progress tracker
    page = requests.get(url if i==1 else url+f"/?page{i}").text
    for title in regex.finditer(page):  #match-uieste toate titlurie din pagina si returneaza un iterator
        for word in [x.lower() for x in page[title.start():title.end()].split(' ') if not ContainsDigit(x) and not ContainsOperator(x) and (x not in ["de", "fara", "cu", "si", "pe", "un", "la", "kg", "km", "în", "ani", "o", "sau", "pentru", "avem", "și", "kw"])]:
            if dict.get(word)!=None:
                dict[word]=dict[word]+1
            else:
                dict[word]=1
print(dict)