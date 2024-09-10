import random

from Classes.Constants import *
from Classes.Materials import Materials
from Classes.TradeOffer import TradeOffer
from Interfaces.BotInterface import BotInterface

# Este bot centra su estrategia en las cartas de desarrollo, y trata de conseguir los máximos puntos y ejércitos
# posibles
# Además, no se detiene a construir ciudades para ahorrar materiales

class EstadosFinitosBot_Cartas(BotInterface):
    """
       Es necesario poner super().nombre_de_funcion() para asegurarse de que coge la función del padre
       """
    town_number = 0
    material_given_more_than_three = None
    # Son los materiales más necesarios en construcciones, luego se piden con year of plenty para tener en mano
    year_of_plenty_material_one = MaterialConstants.CEREAL
    year_of_plenty_material_two = MaterialConstants.MINERAL
    estado_actual = EstadosConstants.CARTAS
    estado_anterior = None

    estado_carretera = 0
    estado_ciudad = 0
    estado_poblado = 0
    estado_cartas = 0

    def __init__(self, bot_id):
        super().__init__(bot_id)

    def on_trade_offer(self, incoming_trade_offer=TradeOffer()):
        """
        Al tratarse de bots que eluden el trade, siempre devuelve que no quiere tradear.
        :param incoming_trade_offer:
        :return:
        """
        if incoming_trade_offer.gives.has_this_more_materials(incoming_trade_offer.receives):
            return False
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
        """
        En los desarrollos de este proyecto, no se va a utilizar la fase de comercio en las partidas.
        """
        return None

    def on_build_phase(self, board_instance):
        # Juega año de la cosecha si l e faltan 2 o 1 materiales para completar una construcción
        # Juega construir carreteras si le da para camino más largo o con ello puede alcanzar un puerto (que no tenga)
        # print('carrtera'+str(self.estado_carretera)+'ciudad'+str(self.estado_ciudad)+'poblado'+str(self.estado_poblado)+'cartas'+str(self.estado_cartas))
        self.board = board_instance

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
                    if self.development_cards_hand.hand[i].effect == DevelopmentCardConstants.ROAD_BUILDING_EFFECT and len(road_possibilities) > 1:
                        return self.development_cards_hand.select_card_by_id(self.development_cards_hand.hand[i].id)
                    else:

                        return self.development_cards_hand.select_card_by_id(self.development_cards_hand.hand[i].id)
        self.change_state()
        match self.estado_actual:
            case EstadosConstants.CARRETERA:
                self.estado_carretera += 1
                if self.hand.resources.has_this_more_materials(BuildConstants.ROAD):
                    possibilities = self.board.valid_road_nodes(self.id)
                    #   construye una carretera aleatoria, el 60% de las veces
                    will_build = random.randint(0, 2)
                    if will_build:
                        if len(possibilities):
                            road_node = random.randint(0, len(possibilities) - 1)
                            return {'building': BuildConstants.ROAD,
                                    'node_id': possibilities[road_node]['starting_node'],
                                    'road_to': possibilities[road_node]['finishing_node']}
            case EstadosConstants.CIUDAD:
                self.estado_ciudad += 1
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
            case EstadosConstants.POBLADO:
                self.estado_poblado += 1
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
            case EstadosConstants.CARTAS:
                self.estado_cartas += 1
                if self.hand.resources.has_this_more_materials(BuildConstants.CARD):
                    return {'building': BuildConstants.CARD}
            case _:
                return None
        # Si tiene materiales para hacer una carta, la construye. Como va la última en la pila,
        #    ya habrá construido cualquier otra cosa más útil
        return None

    def on_game_start(self, board_instance):
        # Si los terrenos adyacentes son materiales distintos, mejor
        # Si el terreno tiene un 6 o un 8 mirar los adyacentes y el siguiente número más cercano a 7
        #   es donde construye la casa si no hay nadie. La carretera se hace apuntando al mar
        self.board = board_instance
        possibilities = self.board.valid_starting_nodes()
        missing = self.missing()
        per_prob = []
        per_diff = []

        # Se generan las variables que tendrán el resultado final
        chosen_node_id = -1
        # chosen_road_to_id = -1
        # Se evalúa que nodos tienen probabilidades cercanas al 7 en algún terreno adyacente
        for node_id in possibilities:
            for terrain_id in self.board.nodes[node_id]['contacting_terrain']:
                if (self.board.terrain[terrain_id]['probability'] == 6 or
                        self.board.terrain[terrain_id]['probability'] == 8):
                    per_prob.append(node_id)

        max_diff = -1
        # Se evalua, dentro de los nodos disponibles, que nodos tienen adyacentes a ellos los máximos materiales posibles.
        # Si se cumple esta regla y la anterior, se insertar en una lista de nodos "perfectos"
        for node_id in possibilities:
            terrains_type = []
            for terrain in self.board.nodes[node_id]['contacting_terrain']:
                if self.board.terrain[terrain]['terrain_type'] not in terrains_type:
                    terrains_type.append(self.board.terrain[terrain]['terrain_type'])
            if len(set(terrains_type)) >= max_diff and self.common_data(list(set(missing)), list(set(
                    terrains_type))) and 2 in terrains_type:
                if per_prob.__contains__(node_id):
                    per_diff.append(node_id)
                    max_diff = len(terrains_type)

        if len(per_diff) > 0:
            chosen_node_id = per_diff[random.randint(0, len(per_diff) - 1)]

        if chosen_node_id == -1 and len(per_prob):
            chosen_node_id = per_prob[random.randint(0, len(per_prob) - 1)]

        # Si no hay ningún nodo ideal, se elige aleatoriamente entre las opciones
        if chosen_node_id == -1:
            chosen_node_id = possibilities[random.randint(0, len(possibilities) - 1)]

        # Sumamos 1 a la cantidad de pueblos creados
        self.town_number += 1

        # Se elige una carretera a un nodo dirección a un oponente entre todas las opciones, si no aleatoria

        adjacent_nodes = self.board.nodes[chosen_node_id]['adjacent']
        possible_roads_torwards_oponent = []

        for node_id in adjacent_nodes:
            adjacent_nodes_lvl_2 = self.board.nodes[node_id]['adjacent']
            for node_id_lvl2 in adjacent_nodes_lvl_2:
                if self.board.nodes[node_id_lvl2]['player'] != -1 and self.board.nodes[node_id_lvl2][
                    'player'] != self.id:
                    possible_roads_torwards_oponent.append(node_id)

        if len(possible_roads_torwards_oponent) > 0:
            chosen_road_to_id = possible_roads_torwards_oponent[
                random.randint(0, len(possible_roads_torwards_oponent) - 1)]
        else:
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

    def change_state(self):
        # Esta clase comprueba si se cumple alguno de los requisitos para cambiar entre estados
        # Estados posibles:
        # Construir ciudades
        # Construir poblados
        # Construir carreteras
        # Conseguir cartas de desarrollo

        estado_nuevo = self.estado_actual
        possibilities = self.board.valid_town_nodes(self.id)
        missing_terrain = self.missing()
        place_to_build_town = self.place_to_build_missing(missing_terrain)
        number_of_roads = self.road_number()

        match self.estado_actual:
            case EstadosConstants.CARRETERA:
                if self.hand.resources.has_this_more_materials(BuildConstants.CARD):
                    estado_nuevo = EstadosConstants.CARTAS
                elif (self.hand.resources.has_this_more_materials(BuildConstants.TOWN) and len(
                            possibilities) != 0) or (len(place_to_build_town) != 0 and missing_terrain != 0):
                        estado_nuevo = EstadosConstants.POBLADO
            case EstadosConstants.POBLADO:
                if self.hand.resources.has_this_more_materials(BuildConstants.CARD):
                    estado_nuevo = EstadosConstants.CARTAS
                elif (not self.hand.resources.has_this_more_materials(BuildConstants.TOWN) or len(
                            possibilities) == 0 or (len(place_to_build_town) != 0 and missing_terrain != 0)):
                        if self.hand.resources.has_this_more_materials(BuildConstants.ROAD) and len(
                                place_to_build_town) == 0 and number_of_roads < 15:
                            estado_nuevo = EstadosConstants.CARRETERA
                        else:
                            estado_nuevo = EstadosConstants.CARTAS
            case EstadosConstants.CARTAS:
                if not self.hand.resources.has_this_more_materials(BuildConstants.CARD):
                    if (self.hand.resources.has_this_more_materials(BuildConstants.TOWN) and len(
                            possibilities) != 0) or (len(place_to_build_town) != 0 and missing_terrain != 0):
                        estado_nuevo = EstadosConstants.POBLADO
                    else:
                        if not self.hand.resources.has_this_more_materials(BuildConstants.ROAD) or len(
                                place_to_build_town) != 0 or number_of_roads >= 15:
                            estado_nuevo = None
                        else:
                            estado_nuevo = EstadosConstants.CARRETERA
            case _:
                estado_nuevo = EstadosConstants.CARTAS
        if self.estado_actual != estado_nuevo:
            self.estado_anterior = self.estado_actual
            self.estado_actual = estado_nuevo
        return None

    def missing(self):

        unique_terrain = []
        sample_terrain = [0, 1, 2, 3, 4]
        nodes = self.board.nodes
        for node_id in nodes:
            terrain = []
            if self.board.nodes[node_id['id']]['player'] == self.id:
                terrain = self.board.__get_contacting_terrain__(node_id['id'])
            for terrain_id in terrain:
                unique_terrain.append(self.board.terrain[terrain_id]['terrain_type'])

        # initialize a null list
        unique_list = []

        # traverse for all elements
        for x in unique_terrain:
            # check if exists in unique_list or not
            if x not in unique_list and x != -1:
                unique_list.append(x)

        missing = []
        for element in sample_terrain:
            if element not in unique_terrain:
                missing.append(element)

        return missing

    def place_to_build_missing(self, missing_terrain):
        list = []
        place_to_build_town = self.board.valid_town_nodes(self.id)
        for node in place_to_build_town:
            contacting_terrain = self.board.__get_contacting_terrain__(node)
            for terrain in contacting_terrain:
                if self.board.terrain[terrain]['terrain_type'] in missing_terrain:
                    list.append(node)
        return list

    def common_data(self, list1, list2):
        result = False
        counter = len(list1)
        found = 0
        found_in_this_loop = False
        if len(list1) > len(list2):
            return True
        # traverse in the 1st list
        for x in list1:
            found_in_this_loop = False
            # traverse in the 2nd list
            for y in list2:

                # if one common
                if x == y:
                    if found_in_this_loop == False:
                        found_in_this_loop = True
                        found += 1
                        if found == counter:
                            result = True
                            return result

        return result

    def road_number(self):
        result = 0
        starting_nodes = []
        end_nodes = []
        for node in self.board.nodes:
            for road in self.board.nodes[node['id']]['roads']:
                if road['player_id'] == self.id and not (
                        (node['id'] in starting_nodes and road['node_id'] in end_nodes) or (
                        road['node_id'] in starting_nodes and node['id'] in end_nodes)):
                    result += 1
                    starting_nodes.append(node['id'])
                    end_nodes.append(road['node_id'])
        return result