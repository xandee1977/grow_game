from random import randint

class Equations():
    # Tamanho do buffer
    options_buffer_size = 3

    # Lista de equacoes
    
    '''
    [
        {'options': [43,35,17,69,97,97], 'result': 35, 'label': '7x5'},
        {'options': [34,38,18,77,89,12], 'result': 18, 'label': '3x6'},
        {'options': [10,5,27,73,55,48], 'result': 10, 'label': '2x5'}
    ]
    '''
    equations = []

    # Equations - Equacoes possiveis
    equations_list = [
        {"label": "1 + 1", "result": 2},
        {"label": "2 x 5", "result": 10},
        {"label": "3 x 6", "result": 18},
        {"label": "7 x 5", "result": 35},
        {"label": "4 x 5", "result": 20}
    ]

    box_list = [
        {"name": "box1", "position_x": 0, "value": randint(0, 99), "element": None},
        {"name": "box2", "position_x": 53,"value": randint(0, 99), "element": None},
        {"name": "box3", "position_x": 106, "value": randint(0, 99), "element": None},
        {"name": "box3", "position_x": 159, "value": randint(0, 99), "element": None},
        {"name": "box4", "position_x": 212, "value": randint(0, 99), "element": None},
        {"name": "box4", "position_x": 265, "value": randint(0, 99), "element": None}
    ]

    def __init__(self):
       print("Starting equation class...")

    # Alimenta a lista equations
    def equations_feed(self):
        while(len(self.equations) < self.options_buffer_size):
            # Sorteio de equacoes
            self.equations_single_feed()
        '''
        print(self.equations)
        text_file = open("debug.txt", "w")
        text_file.write(str(self.equations))
        text_file.close()
        '''
    
    # Adiciona um item na lista de equacoes
    def equations_single_feed(self):
        print("equations_single_feed... ")
        # Equacao sorteada
        eq_key = randint(0, (len(self.equations_list)-1))
        # Box que tera a resposta
        res_key = randint(0, (len(self.box_list)-1))

        # Lista de opcoes
        cur_opt_list = []

        # Sorteando as opcoes dos box       
        for box in self.box_list:
            if len(cur_opt_list) == res_key:
                cur_opt_list.append(self.equations_list[eq_key]["result"])
            else:
                cur_opt_list.append(randint(0, 99))

        self.equations.append({
            "label": self.equations_list[eq_key]["label"],
            "result": self.equations_list[eq_key]["result"],
            "options": cur_opt_list
        })        

    def run(self):
        self.equations_feed()
