import timeit
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
def InsertIntoRanking(word, frequency):
    global maxes, words
    stack1 = [] #stack-like structure
    stack2 = [] #stack-like structure
    height = len(maxes) #numarul filtrelor initiale
    if height==0 or height<10 and frequency<maxes[height-1]: #daca nu e nimic in "maxes" sau daca nu sunt deja 10 valori si frecventa e mai mica decat cea mai mica,
        maxes.append(frequency) # pur si simplu pun cuvantul si frecventa
        words.append(word)
    elif frequency>maxes[height-1]:
        while len(maxes)>0 and frequency>maxes[len(maxes)-1]: #scot din "maxes" cat timp mai exista ceva de scos sau pana frecventa isi gaseste locul
            stack1.append(maxes.pop())
            stack2.append(words.pop())
        maxes.append(frequency) #pun in stiva frecventa si cuvantul asociat pe pozitia de drept
        words.append(word)
        for i in range(len(stack1)-1, -1, -1): #parcurg cuvintele scoase din "maxes"
            if len(maxes)==10:
                return
            if stack2[i]!=word: #si le pun inapoi decat daaca nu sunt duplicate si pana am umplut "maxes" cu 10 valori
                maxes.append(stack1[i])
                words.append(stack2[i])
    return
            

url = "https://www.olx.ro/d/anunturi-agricole" #url-ul paginii de start
regex = re.compile('(?s)(?<=<h6 class=\"css-v3vynn-Text eu5v0x0\">).*?(?=</h6>)') #regex-ul pentru preluarea titlurilor
forbidden_words = ["de", "fara", "cu", "si", "pe", "un", "la", "kg", "km", "în", "ani", "o", "sau", "pentru", "avem", "și", "kw", "", "vand", "vând", "noi"]
dict={} #dictionar pentru accesarea rapida a titlurilor si frecventelor ascoiate
maxes = [] #cele 10 cele mai mari frecvente
words = [] #cele 10 cele mai frecvente cuvinte
start = timeit.default_timer()
for i in range(1, 26): #25 de pagini max are OLX-ul
    print("page ",i) #improv progress tracker
    page = requests.get(url if i==1 else url+f"/?page{i}").text
    for title in regex.finditer(page):  #match-uieste toate titlurie din pagina si returneaza un iterator
        for word in [x.lower() for x in page[title.start():title.end()].split(' ') if not ContainsDigit(x) and not ContainsOperator(x) and (x.lower() not in forbidden_words)]:
            if dict.get(word)!=None:
                dict[word]=dict[word]+1
            else:
                dict[word]=1
            InsertIntoRanking(word, dict[word])
end = timeit.default_timer()
print(f"Done in {end - start} seconds!\n")
for i in range(10):
    print(words[i], maxes[i])
