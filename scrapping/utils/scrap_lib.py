from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
from nltk.tokenize import sent_tokenize

def get_bs4_for_word(word):
    '''
    Get the BeautifullSoup object for determined word
    '''
    try:
        if ' ' in word:
            word.replace(' ', '+')
        
        url = urlopen(f"https://www.linguee.com/english-french/translation/{word}.html")
        bs = BeautifulSoup(url.read(), 'lxml')
        return bs
    except URLError:
        print("It was not possible to open the URL for determined word. Try checking any typos")
    except HTTPError:
        print("It was not possible to process the website (used 'lxml') ")

def get_direct_translations(bs):
    direct_translation = bs.find_all('h3', {'class':'translation_desc'})
    translations = []
    for item in direct_translation:
        translations.append(str(item.get_text()))
    return [sent_tokenize(translation) for translation in translations]

def get_examples(bs):
    examples_lines = bs.find_all('div', {'class':'example_lines'})
    examples = []
    for item in examples_lines:
        examples.append(item.get_text())