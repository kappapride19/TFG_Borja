import random

from Classes.Constants import *
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Interfaces.BotInterface import BotInterface


class AdrianHerasBot_sinComercio(BotInterface):
    """
    Es necesario poner super().nombre_de_funcion() para asegurarse de que coge la función del padre
    """
    town_number = 0
    material_given_more_than_three = None
    # Son los materiales más necesarios en construcciones, luego se piden con year of plenty para tener en mano
    year_of_plenty_material_one = MaterialConstants.CEREAL
    year_of_plenty_material_two = MaterialConstants.MINERAL

    def __init__(self, bot_id):
        super().__init__(bot_id)

    def on_trade_offer(self, incoming_trade_offer=TradeOffer()):
        """
        Hay que tener en cuenta que gives se refiere a los materiales que da el jugador que hace la oferta,
        luego en este caso es lo que recibe
        :param incoming_trade_offer:
        :return:
        """
        if incoming_trade_offer.gives.has_this_more_materials(incoming_trade_offer.receives):
            return True
        else:
            return False
        # return super().on_trade_offer(incoming_trade_offer)

    def on_turn_start(self):
        # Si tiene mano de cartas de desarrollo
        if len(self.development_cards_hand.check_hand()):
            # Mira todas las cartas
            for i in range(0, len(self.development_cards_hand.check_hand())):
                # Si una es un caballero
                if self.development_cards_hand.hand[i].type == DevelopmentCardConstants.KNIGHT:
                    # La juega
                    return self.development_cards_hand.select_card_by_id(self.development_cards_hand.hand[i].id)
        return None

    def on_having_more_than_7_materials_when_thief_is_called(self):
        # Comprueba si tiene materiales para construir una ciudad. Si los tiene, descarta el resto que no le sirvan.
        if self.hand.resources.has_this_more_materials(BuildConstants.CITY):
            while self.hand.get_total() > 7:
                if self.hand.resources.wool > 0:
                    self.hand.remove_material(4, 1)

                if self.hand.resources.cereal > 2:
                    self.hand.remove_material(0, 1)
                if self.hand.resources.mineral > 3:
                    self.hand.remove_material(1, 1)

                if self.hand.resources.clay > 0:
                    self.hand.remove_material(2, 1)
                if self.hand.resources.wood > 0:
                    self.hand.remove_material(3, 1)
        # Si no tiene materiales para hacer una ciudad descarta de manera aleatoria cartas de su mano
        return self.hand

    def on_moving_thief(self):
        # Bloquea un número 6 u 8 donde no tenga un pueblo, pero que tenga uno del rival
        # Si no se dan las condiciones lo deja donde está, lo que hace que el GameManager lo ponga en un lugar aleatorio
        terrain_with_thief_id = -1
        for terrain in self.board.terrain:
            if not terrain['has_thief']:
                if terrain['probability'] == 6 or terrain['probability'] == 8:
                    nodes = self.board.__get_contacting_nodes__(terrain['id'])
                    has_own_town = False
                    has_enemy_town = False
                    enemy = -1
                    for node_id in nodes:
                        if self.board.nodes[node_id]['player'] == self.id:
                            has_own_town = True
                            break
                        if self.board.nodes[node_id]['player'] != -1:
                            has_enemy_town = True
                            enemy = self.board.nodes[node_id]['player']

                    if not has_own_town and has_enemy_town:
                        return {'terrain': terrain['id'], 'player': enemy}
            else:
                terrain_with_thief_id = terrain['id']

        return {'terrain': terrain_with_thief_id, 'player': -1}

    def on_turn_end(self):
        # Si tiene mano de cartas de desarrollo
        if len(self.development_cards_hand.check_hand()):
            # Mira todas las cartas
            for i in range(0, len(self.development_cards_hand.check_hand())):
                # Si una es un punto de victoria
                if self.development_cards_hand.hand[i].type == DevelopmentCardConstants.VICTORY_POINT:
                    # La juega
                    return self.development_cards_hand.select_card_by_id(self.development_cards_hand.hand[i].id)
        return None

    def on_commerce_phase(self):
        return None

    def on_build_phase(self, board_instance):
        # Juega año de la cosecha si le faltan 2 o 1 materiales para completar una construcción
        # Juega construir carreteras si le da para camino más largo o con ello puede alcanzar un puerto (que no tenga)
        self.board = board_instance
        number_of_roads = self.road_number()

        # Si tiene mano de cartas de desarrollo
        if len(self.development_cards_hand.check_hand()):
            # Mira todas las cartas
            for i in range(0, len(self.development_cards_hand.check_hand())):
                # Comprueba primero de que hay más de 2 carreteras disponibles para construirlas
                road_possibilities = self.board.valid_road_nodes(self.id)

                # Si una es año de la cosecha o construir carreteras y hay al menos 2 carreteras disponibles a construir
                if (self.development_cards_hand.hand[i].effect == DevelopmentCardConstants.YEAR_OF_PLENTY_EFFECT or
                        (self.development_cards_hand.hand[i].effect == DevelopmentCardConstants.ROAD_BUILDING_EFFECT and
                         len(road_possibilities) > 1)):
                    # La juega
                    return self.development_cards_hand.select_card_by_id(self.development_cards_hand.hand[i].id)

        if self.hand.resources.has_this_more_materials(BuildConstants.CITY) and self.town_number > 0:
            possibilities = self.board.valid_city_nodes(self.id)
            for node_id in possibilities:
                for terrain_piece_id in self.board.nodes[node_id]['contacting_terrain']:
                    # Hacemos una ciudad solo si la probabilidad de que salga el número es mayor o igual a 4/36
                    if self.board.terrain[terrain_piece_id]['probability'] == 5 or \
                            self.board.terrain[terrain_piece_id]['probability'] == 6 or \
                            self.board.terrain[terrain_piece_id]['probability'] == 8 or \
                            self.board.terrain[terrain_piece_id]['probability'] == 9:
                        self.town_number -= 1  # Transformamos un pueblo en una ciudad
                        return {'building': BuildConstants.CITY, 'node_id': node_id}

        if self.hand.resources.has_this_more_materials(BuildConstants.TOWN):
            possibilities = self.board.valid_town_nodes(self.id)
            for node_id in possibilities:
                for terrain_piece_id in self.board.nodes[node_id]['contacting_terrain']:
                    # Hacemos un pueblo solo si la probabilidad de que salga el número es mayor o igual a 3/36
                    # O si el nodo es costero y posee un puerto
                    if self.board.terrain[terrain_piece_id]['probability'] == 4 or \
                            self.board.terrain[terrain_piece_id]['probability'] == 5 or \
                            self.board.terrain[terrain_piece_id]['probability'] == 6 or \
                            self.board.terrain[terrain_piece_id]['probability'] == 8 or \
                            self.board.terrain[terrain_piece_id]['probability'] == 9 or \
                            self.board.terrain[terrain_piece_id]['probability'] == 10:
                        self.town_number += 1  # Añadimos un pueblo creado
                        return {'building': BuildConstants.TOWN, 'node_id': node_id}

        if self.hand.resources.has_this_more_materials(BuildConstants.ROAD) and number_of_roads < 15:
            # Construye sí o sí carretera si acaba en un nodo costero, pero, ¿y si no lo busca aleatoriamente?
            # Idealmente, debe de poder buscar caminos y encontrar el ideal a un puerto o similar, pero eso implicaría
            #  programar un algoritmo de búsqueda de nodos por pesos que actualmente me parece imposible de hacer.

            # Comprobar qué caminos posibles hay para cada nodo. Escoger el más alto si el ID del nodo es 32 o más.
            # Más bajo si es menor hacer override de eso si uno de los dos es directamente costero

            # TODO: Sería ideal que funcionase pero hay poco tiempo, que coja una aleatoria, pero si es costero y tiene puerto lo coge siempre
            possibilities = self.board.valid_road_nodes(self.id)
            for road_obj in possibilities:
                if self.board.is_it_a_coastal_node(road_obj['finishing_node']) and \
                        self.board.nodes[road_obj['finishing_node']]['harbor'] != HarborConstants.NONE:
                    return {'building': BuildConstants.ROAD,
                            'node_id': road_obj['starting_node'],
                            'road_to': road_obj['finishing_node']}

            # Asumiendo que no hay ninguna ideal (es decir, robarse los puertos),
            #   construye una carretera aleatoria, el 60% de las veces
            will_build = random.randint(0, 2)
            if will_build:
                if len(possibilities):
                    road_node = random.randint(0, len(possibilities) - 1)
                    return {'building': BuildConstants.ROAD,
                            'node_id': possibilities[road_node]['starting_node'],
                            'road_to': possibilities[road_node]['finishing_node']}

        # Si tiene materiales para hacer una carta, la construye. Como va la última en la pila,
        #    ya habrá construido cualquier otra cosa más útil
        if self.hand.resources.has_this_more_materials(BuildConstants.CARD):
            return {'building': BuildConstants.CARD}

        return None

    def on_game_start(self, board_instance):
        # Si el terreno tiene un 6 o un 8 mirar los adyacentes y el siguiente número más cercano a 7
        #   es donde construye la casa si no hay nadie. La carretera se hace apuntando al mar
        self.board = board_instance
        possibilities = self.board.valid_starting_nodes()
        # Se generan las variables que tendrán el resultado final
        chosen_node_id = -1
        # chosen_road_to_id = -1
        for node_id in possibilities:
            for terrain_id in self.board.nodes[node_id]['contacting_terrain']:
                if (self.board.terrain[terrain_id]['probability'] == 6 or
                        self.board.terrain[terrain_id]['probability'] == 8):
                    chosen_node_id = node_id

        # Si no hay ningún nodo ideal, se elige aleatoriamente entre las opciones
        if chosen_node_id == -1:
            chosen_node_id = possibilities[random.randint(0, len(possibilities) - 1)]

        # Sumamos 1 a la cantidad de pueblos creados
        self.town_number += 1

        # Se elige una carretera aleatoria entre todas las opciones
        possible_roads = self.board.nodes[chosen_node_id]['adjacent']
        chosen_road_to_id = possible_roads[random.randint(0, len(possible_roads) - 1)]

        return chosen_node_id, chosen_road_to_id

    def on_monopoly_card_use(self):
        # Elige el material que más haya intercambiado (variable global de esta clase)
        return self.material_given_more_than_three

    # noinspection DuplicatedCode
    def on_road_building_card_use(self):
        # Elige dos carreteras aleatorias entre las opciones
        valid_nodes = self.board.valid_road_nodes(self.id)
        # Se supone que solo se ha usado la carta si hay más de 2 carreteras disponibles a construir,
        # pero se dejan por si acaso
        if len(valid_nodes) > 1:
            while True:
                road_node = random.randint(0, len(valid_nodes) - 1)
                road_node_2 = random.randint(0, len(valid_nodes) - 1)
                if road_node != road_node_2:
                    return {'node_id': valid_nodes[road_node]['starting_node'],
                            'road_to': valid_nodes[road_node]['finishing_node'],
                            'node_id_2': valid_nodes[road_node_2]['starting_node'],
                            'road_to_2': valid_nodes[road_node_2]['finishing_node'],
                            }
        elif len(valid_nodes) == 1:
            return {'node_id': valid_nodes[0]['starting_node'],
                    'road_to': valid_nodes[0]['finishing_node'],
                    'node_id_2': None,
                    'road_to_2': None,
                    }
        return None

    def on_year_of_plenty_card_use(self):
        return {'material': self.year_of_plenty_material_one, 'material_2': self.year_of_plenty_material_two}

    def road_number(self):
            result = 0
            starting_nodes = []
            end_nodes = []
            for node in self.board.nodes:
                for road in self.board.nodes[node['id']]['roads']:
                    if road['player_id'] == self.id and not ((node['id'] in starting_nodes and road['node_id'] in end_nodes) or (road['node_id'] in starting_nodes and node['id'] in end_nodes)):
                        result += 1
                        starting_nodes.append(node['id'])
                        end_nodes.append(road['node_id'])
            return result