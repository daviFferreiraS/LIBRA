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
        return json.dumps(transform, sort_keys= True, ensure_ascii= True, indent=2)
