import json

class Word():
     def __init__(self, french):
        self.english = None
        self.french = french
        self.examples = None
        self.plus_rare = None # Palavras menos usuais
    
     def to_dict(self):
        return {
             'english' : self.english,
             'french' : self.french,
             'examples' : self.examples
        }
     
     def dump(self):
        transform = self.to_dict()
        return json.dumps(transform, sort_keys= True, ensure_ascii= False)



# salvar as informações em um arq JSON, JSONline (ideal, dá pra fazer na mão, mas tem um pacote tbm),
# csv
# pegar as palavras de um sample da wikipedia
    # fazer um downsampling
    # buscar todas essas palavras do downsampling no linguee