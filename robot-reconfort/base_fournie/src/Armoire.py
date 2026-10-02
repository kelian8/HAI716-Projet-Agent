class Armoire:
    def __init__(self,depart:(int,int)):
        self.current_casier = depart
        self.casiers = []
        for row in range(3):
            self.casiers.append([])
            for col in range(8):
                self.casiers[row].append(-1)

    def add_objet(self,intensite_row:int,emotion_col:int,objet:str):
        self.casiers[intensite_row][emotion_col] = objet
