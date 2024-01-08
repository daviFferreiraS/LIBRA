from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
from nltk.tokenize import sent_tokenize, WhitespaceTokenizer

def get_bs4_for_word(word):
    '''
    Get the BeautifullSoup object for determined word
    '''
    try:
        if ' ' in word:
            word.replace(' ', '+')
        
        url = urlopen(f"https://www.linguee.com/french-english/translation/{word}.html")
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
    tk_translations = [sent_tokenize(translation) for translation in translations]

    result = []
    for translation in tk_translations:
        result.append(translation[0])
    
    return result

def get_examples(bs):
    tk = WhitespaceTokenizer()
    examples_lines = bs.find_all('div', {'class':'example_lines'})
    examples = []
    for item in examples_lines:
        examples.append(item.get_text())
        
    tokenized_examples = [tk.tokenize(example) for example in examples]

    examples = []

    for t_example in tokenized_examples:
        examples.append(form_example_phrase(t_example))
    
    return filter_unwanted_phrases(examples)

def form_example_phrase(example): ## only needed because the bs4 object return several /n/n/n/n amidst the words
    phrase = ""
    for word in example:
        phrase += word + " "
    
    return phrase

def filter_unwanted_phrases(examples): ## if the phrase is located, it's prefered for now to discart the example
    unwanted = ['See alternative translations', 'Examples']

    cpy_examples = examples.copy()
    for index, example in enumerate(examples): 
        if example in unwanted:
            cpy_examples.pop(index)

    return cpy_examples
    