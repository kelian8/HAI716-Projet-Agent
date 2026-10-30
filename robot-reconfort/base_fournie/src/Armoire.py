class Armoire:
    def __init__(self,depart:tuple[int,int]):
        self.casier_depart = depart
        self.casiers:list[list[str|None]] = []
        for row in range(3):
            self.casiers.append([])
            for col in range(8):
                self.casiers[row].append(None)

    def add_objet(self,intensite_row:int,emotion_col:int,objet:str | None):
        self.casiers[intensite_row][emotion_col] = objet

    def get_objet(self,intensite_row:int,emotion_col:int):
        return self.casiers[intensite_row][emotion_col]
