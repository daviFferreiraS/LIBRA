class Word():
     def __init__(self, english):
        self.english = english
        self.french = None
        self.examples = None
        self.plus_rare = None # Palavras menos usuais
    
     def to_dict(self):
        string1 = ""
        for definition in self.french:
            string1 += definition[0] + ','
        
        string2 = ""
        for example in self.examples:
            string2 += example[0] + ','
        

        return {
             'english' : self.english,
             'french' : string1,
             'examples' : string2
        }



# salvar as informações em um arq JSON, JSONline (ideal, dá pra fazer na mão, mas tem um pacote tbm),
# csv
# pegar as palavras de um sample da wikipedia
    # fazer um downsampling
    # buscar todas essas palavras do downsampling no linguee