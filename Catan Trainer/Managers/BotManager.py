from random import randrange, choices, random
import random
from Bots import RandomBot, AlexPastorBot, AdrianHerasBot_sinComercio, EstadosFinitosBot_Pasivo, EstadosFinitosBot_Cartas,EstadosFinitosBot_Agresivo, EstadosFinitosBot
from Classes.DevelopmentCards import DevelopmentCardsHand
from Classes.Hand import Hand
from Classes.Constants import *


class BotManager:
    """
    Clase que se encarga de los bots. De momento solo los carga en la partida, sin embargo, cabe la posibilidad de que
    sea el bot manager el que se encargue de darle paso a los bots a hacer sus turnos
    """
    j_lista_pesos = [[1, 1, 1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1],
                     [1, 1, 1, 1]]



    j_lista_pesos_real = [[25, 25, 25, 25],
                          [25, 25, 25, 25],
                          [25, 25, 25, 25],
                          [25, 25, 25, 25]]

    # j_lista_pesos_no_real = [[6, 82, 6, 6], [82, 6, 6, 6], [82, 6, 6, 6], [6, 6, 82, 6]]

    # j_lista_pesos_real = [[6,82, 6, 6], [82, 6, 6, 6], [82, 6, 6, 6], [6, 6, 82, 6]]

    j_self_decided_class = [False, False, False, False]

    actual_player = 0
    first_bot_class = ''
    second_bot_class = ''
    third_bot_class = ''
    fourth_bot_class = ''
    wins_Agresivo = 0
    wins_Pasiva = 0
    wins_Cartas = 0
    wins_Aleatorio = 0
    players = []

    def __init__(self, for_test=False, for_advanced=False):
        if not for_test and not for_advanced:
            self.first_bot_class = self.import_bot_class_from_input('primer')
            self.second_bot_class = self.import_bot_class_from_input('segundo')
            self.third_bot_class = self.import_bot_class_from_input('tercer')
            self.fourth_bot_class = self.import_bot_class_from_input('cuarto')
            #for advanced


        elif for_test == 'test_específico':
            self.first_bot_class = AlexPastorBot.AlexPastorBot
            self.second_bot_class = AlexPastorBot.AlexPastorBot
            self.third_bot_class = AlexPastorBot.AlexPastorBot
            self.fourth_bot_class = AlexPastorBot.AlexPastorBot
        elif for_advanced:
            my_list = ['EstadosFinitosBot_Agresivo', 'EstadosFinitosBot_Pasivo', 'EstadosFinitosBot_Cartas',
                       'RandomBot']
            primer = choices(my_list, [25, 25, 25, 25], k=1)[0]
            segundo = choices(my_list, [25, 25, 25, 25], k=1)[0]
            tercer = choices(my_list, [25, 25, 25, 25], k=1)[0]
            cuarto = choices(my_list, [25, 25, 25, 25], k=1)[0]
            self.first_bot_class = getattr(__import__('Bots.' + primer, fromlist=[primer]), primer)
            self.second_bot_class = getattr(__import__('Bots.' + segundo, fromlist=[segundo]), segundo)
            self.third_bot_class = getattr(__import__('Bots.' + tercer, fromlist=[tercer]), tercer)
            self.fourth_bot_class = getattr(__import__('Bots.' + cuarto, fromlist=[cuarto]), cuarto)
        else:
            self.first_bot_class = RandomBot.RandomBot
            self.second_bot_class = RandomBot.RandomBot
            self.third_bot_class = RandomBot.RandomBot
            self.fourth_bot_class = RandomBot.RandomBot

        self.reset_game_values()
        return

    def set_actual_player(self, player_id=0):
        """
        :param player_id: int
        :return: None
        """
        self.actual_player = player_id
        return

    def reset_game_values(self, for_advanced=False, winner= -1):
        if not for_advanced:
            self.players = [
                {
                    'id': 0,
                    'victory_points': 0,
                    'hidden_victory_points': 0,
                    'player': self.first_bot_class(0),
                    'resources': Hand(),
                    'development_cards': DevelopmentCardsHand(),
                    'knights': 0,
                    'already_played_development_card': 0,
                    'largest_army': 0,
                    'longest_road': 0,
                },
                {
                    'id': 1,
                    'victory_points': 0,
                    'hidden_victory_points': 0,
                    'player': self.second_bot_class(1),
                    'resources': Hand(),
                    'development_cards': DevelopmentCardsHand(),
                    'knights': 0,
                    'already_played_development_card': 0,
                    'largest_army': 0,
                    'longest_road': 0,
                },
                {
                    'id': 2,
                    'victory_points': 0,
                    'hidden_victory_points': 0,
                    'player': self.third_bot_class(2),
                    'resources': Hand(),
                    'development_cards': DevelopmentCardsHand(),
                    'knights': 0,
                    'already_played_development_card': 0,
                    'largest_army': 0,
                    'longest_road': 0,
                },
                {
                    'id': 3,
                    'victory_points': 0,
                    'hidden_victory_points': 0,
                    'player': self.fourth_bot_class(3),
                    'resources': Hand(),
                    'development_cards': DevelopmentCardsHand(),
                    'knights': 0,
                    'already_played_development_card': 0,
                    'largest_army': 0,
                    'longest_road': 0,
                }
            ]
        else:
                if winner != -1:
                    # posibilities = [EstadosFinitosBot_Pasivo.EstadosFinitosBot_Pasivo, EstadosFinitosBot_Cartas.EstadosFinitosBot_Cartas,EstadosFinitosBot_Agresivo.EstadosFinitosBot_Agresivo]ç

                    match winner:
                        case 0:
                            winnerclass = self.first_bot_class
                        case 1:
                            winnerclass = self.second_bot_class
                        case 2:
                            winnerclass = self.third_bot_class
                        case 3:
                            winnerclass = self.fourth_bot_class


                    match winnerclass:
                        case EstadosFinitosBot_Pasivo.EstadosFinitosBot_Pasivo:
                            self.j_lista_pesos[winner][1]+=1
                            #self.j_lista_pesos_no_real[winner][1] += 1
                            self.wins_Pasiva+=1
                        case EstadosFinitosBot_Cartas.EstadosFinitosBot_Cartas:
                            self.j_lista_pesos[winner][2]+=1
                            #self.j_lista_pesos_no_real[winner][2] += 1
                            self.wins_Cartas += 1
                        case EstadosFinitosBot_Agresivo.EstadosFinitosBot_Agresivo:
                            self.j_lista_pesos[winner][0]+=1
                            #self.j_lista_pesos_no_real[winner][0] += 1
                            self.wins_Agresivo += 1
                        case _:
                            self.j_lista_pesos[winner][3]+=1
                            #self.j_lista_pesos_no_real[winner][3] += 1
                            self.wins_Aleatorio += 1


                my_list = ['EstadosFinitosBot_Agresivo', 'EstadosFinitosBot_Pasivo', 'EstadosFinitosBot_Cartas','RandomBot']
                self.create_weights()
                #self.create_weights_modificado()
                answer = random.randint(0, 5)
                #answer = 0
                if answer != 0:
                    primer =choices(my_list, self.j_lista_pesos_real[0], k=1)[0]
                    self.j_self_decided_class[0] = True
                else:
                    primer = choices(my_list, [25, 25, 25, 25], k=1)[0]
                    self.j_self_decided_class[0] = False

                answer = random.randint(0, 1)
                if answer != 0:
                    segundo = choices(my_list, self.j_lista_pesos_real[1], k=1)[0]
                    self.j_self_decided_class[1] = True
                else:
                    segundo = choices(my_list, [25, 25, 25, 25], k=1)[0]
                    self.j_self_decided_class[1] = False

                answer = random.randint(0, 1)
                if answer != 0:
                    tercer = choices(my_list, self.j_lista_pesos_real[2], k=1)[0]
                    self.j_self_decided_class[2] = True
                else:
                    tercer = choices(my_list, [25, 25, 25, 25], k=1)[0]
                    self.j_self_decided_class[2] = False

                answer = random.randint(0, 1)
                if answer != 0:
                    cuarto = choices(my_list, self.j_lista_pesos_real[3], k=1)[0]
                    self.j_self_decided_class[3] = True
                else:
                    cuarto = choices(my_list, [1, 1, 1, 1], k=1)[0]
                    self.j_self_decided_class[3] = False

                self.first_bot_class = getattr(__import__('Bots.' + primer, fromlist=[primer]), primer)
                self.second_bot_class = getattr(__import__('Bots.' + segundo, fromlist=[segundo]), segundo)
                self.third_bot_class = getattr(__import__('Bots.' + tercer, fromlist=[tercer]), tercer)
                self.fourth_bot_class = getattr(__import__('Bots.' + cuarto, fromlist=[cuarto]), cuarto)


                self.players = [
                    {
                        'id': 0,
                        'victory_points': 0,
                        'hidden_victory_points': 0,
                        'player': self.first_bot_class(0),
                        'resources': Hand(),
                        'development_cards': DevelopmentCardsHand(),
                        'knights': 0,
                        'already_played_development_card': 0,
                        'largest_army': 0,
                        'longest_road': 0,
                    },
                    {
                        'id': 1,
                        'victory_points': 0,
                        'hidden_victory_points': 0,
                        'player': self.second_bot_class(1),
                        'resources': Hand(),
                        'development_cards': DevelopmentCardsHand(),
                        'knights': 0,
                        'already_played_development_card': 0,
                        'largest_army': 0,
                        'longest_road': 0,
                    },
                    {
                        'id': 2,
                        'victory_points': 0,
                        'hidden_victory_points': 0,
                        'player': self.third_bot_class(2),
                        'resources': Hand(),
                        'development_cards': DevelopmentCardsHand(),
                        'knights': 0,
                        'already_played_development_card': 0,
                        'largest_army': 0,
                        'longest_road': 0,
                    },
                    {
                        'id': 3,
                        'victory_points': 0,
                        'hidden_victory_points': 0,
                        'player': self.fourth_bot_class(3),
                        'resources': Hand(),
                        'development_cards': DevelopmentCardsHand(),
                        'knights': 0,
                        'already_played_development_card': 0,
                        'largest_army': 0,
                        'longest_road': 0,
                    }
                ]

        return

    def import_bot_class_from_input(self, name=''):
        module_class = input(
            'Módulo y clase del ' + name + ' bot (ej: mymodule.myclass)(dejar en blanco para usar la por defecto): ')
        if module_class == '':
            klass = RandomBot.RandomBot
        else:
            components = module_class.split('.')
            module = __import__('Bots.' + components[0], fromlist=[components[1]])
            klass = getattr(module, components[1])

        return klass

    def get_victories(self):
        return {'Victorias del bot agresivo' : self.wins_Agresivo, 'Victorias del bot pasivo' : self.wins_Pasiva, 'Victorias del bot cartas' : self.wins_Cartas, 'Victorias del vot aleatorio' : self.wins_Aleatorio}

    def get_classes(self):
        return {'J0' :
                    {
                        'Clase seleccionada': str(self.first_bot_class) ,
                        'Seleccionada de forma aleatoria?': str(not self.j_self_decided_class[0]),
                        'Matriz de victorias en esta partida:': str(self.j_lista_pesos[0]),
                    'Matriz de pesos en esta partida' :  str(self.j_lista_pesos_real[0])} ,
            'J1':
                {
                    'Clase seleccionada': str(self.second_bot_class),
                    'Seleccionada de forma aleatoria?': str(not self.j_self_decided_class[1]),
                    'Matriz de victorias en esta partida:': str(self.j_lista_pesos[1]),
                    'Matriz de pesos en esta partida' :  str(self.j_lista_pesos_real[1])},
            'J2':
                {
                    'Clase seleccionada': str(self.third_bot_class),
                    'Seleccionada de forma aleatoria?': str(not self.j_self_decided_class[2]),
                    'Matriz de victorias en esta partida:': str(self.j_lista_pesos[2]),
                    'Matriz de pesos en esta partida' :  str(self.j_lista_pesos_real[2])},
            'J3':
                {
                    'Clase seleccionada': str(self.fourth_bot_class),
                    'Seleccionada de forma aleatoria?': str(not self.j_self_decided_class[3]),
                    'Matriz de victorias en esta partida:': str(self.j_lista_pesos[3]),
                    'Matriz de pesos en esta partida' :  str(self.j_lista_pesos_real[3])}
        }

    def create_weights(self):

        total_first = self.j_lista_pesos[0][0] + self.j_lista_pesos[0][1] + self.j_lista_pesos[0][2] + self.j_lista_pesos[0][3]
        total_second = self.j_lista_pesos[1][0] + self.j_lista_pesos[1][1] + self.j_lista_pesos[1][2] + self.j_lista_pesos[1][3]
        total_third = self.j_lista_pesos[2][0] + self.j_lista_pesos[2][1] + self.j_lista_pesos[2][2] + self.j_lista_pesos[2][3]
        total_fourth = self.j_lista_pesos[3][0] + self.j_lista_pesos[3][1] + self.j_lista_pesos[3][2] + self.j_lista_pesos[3][3]
        self.j_lista_pesos_real = [[self.j_lista_pesos[0][0]/total_first*100, self.j_lista_pesos[0][1]/total_first*100,self.j_lista_pesos[0][2]/total_first*100,self.j_lista_pesos[0][3]/total_first*100],
                                   [self.j_lista_pesos[1][0] / total_second * 100, self.j_lista_pesos[1][1] / total_second * 100, self.j_lista_pesos[1][2] / total_second * 100, self.j_lista_pesos[1][3] / total_second * 100],
                                   [self.j_lista_pesos[2][0]/total_third*100, self.j_lista_pesos[2][1]/total_third*100,self.j_lista_pesos[2][2]/total_third*100,self.j_lista_pesos[2][3]/total_third*100],
                                   [self.j_lista_pesos[3][0] / total_fourth * 100,self.j_lista_pesos[3][1] / total_fourth * 100,self.j_lista_pesos[3][2] / total_fourth * 100,self.j_lista_pesos[3][3] / total_fourth * 100]]

        return

    def create_weights_modificado(self):

        total_first = self.j_lista_pesos_no_real[0][0] + self.j_lista_pesos_no_real[0][1] + \
                      self.j_lista_pesos_no_real[0][2] + self.j_lista_pesos_no_real[0][3]
        total_second = self.j_lista_pesos_no_real[1][0] + self.j_lista_pesos_no_real[1][1] + \
                       self.j_lista_pesos_no_real[1][2] + self.j_lista_pesos_no_real[1][3]
        total_third = self.j_lista_pesos_no_real[2][0] + self.j_lista_pesos_no_real[2][1] + \
                      self.j_lista_pesos_no_real[2][2] + self.j_lista_pesos_no_real[2][3]
        total_fourth = self.j_lista_pesos_no_real[3][0] + self.j_lista_pesos_no_real[3][1] + \
                       self.j_lista_pesos_no_real[3][2] + self.j_lista_pesos_no_real[3][3]
        self.j_lista_pesos_real = [
            [self.j_lista_pesos_no_real[0][0] / total_first * 100, self.j_lista_pesos_no_real[0][1] / total_first * 100,
             self.j_lista_pesos_no_real[0][2] / total_first * 100,
             self.j_lista_pesos_no_real[0][3] / total_first * 100],
            [self.j_lista_pesos_no_real[1][0] / total_second * 100,
             self.j_lista_pesos_no_real[1][1] / total_second * 100,
             self.j_lista_pesos_no_real[1][2] / total_second * 100,
             self.j_lista_pesos_no_real[1][3] / total_second * 100],
            [self.j_lista_pesos_no_real[2][0] / total_third * 100, self.j_lista_pesos_no_real[2][1] / total_third * 100,
             self.j_lista_pesos_no_real[2][2] / total_third * 100,
             self.j_lista_pesos_no_real[2][3] / total_third * 100],
            [self.j_lista_pesos_no_real[3][0] / total_fourth * 100,
             self.j_lista_pesos_no_real[3][1] / total_fourth * 100,
             self.j_lista_pesos_no_real[3][2] / total_fourth * 100,
             self.j_lista_pesos_no_real[3][3] / total_fourth * 100]]

        return