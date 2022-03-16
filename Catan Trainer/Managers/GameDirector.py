from Managers.GameManager import GameManager


class GameDirector:
    """
    Clase que se encarga de dirigir la partida, empezarla y acabarla
    """
    # turn_manager = TurnManager()
    # bot_manager = BotManager()
    game_manager = GameManager()

    def __init__(self):
        return

    # Turn #
    def start_turn(self, player=-1):
        """
        Esta función permite iniciar el turno
        :param player: número que representa al jugador
        :return: void
        """
        print('----------')
        print('start turn: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(0)
        self.game_manager.bot_manager.set_actual_player(player)

        self.game_manager.throw_dice()
        self.game_manager.give_resources()

        print('Jugador: ' + str(self.game_manager.turn_manager.get_whose_turn_is_it()))
        self.game_manager.bot_manager.actualPlayer.on_turn_start()
        return

    def start_commerce_phase(self, player=-1):
        """
        Esta función permite pasar a la fase de comercio
        :param player: número que representa al jugador
        :return: void
        """
        print('start commerce phase: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(1)
        trade_offer = self.game_manager.bot_manager.actualPlayer.on_commerce_phase()
        if trade_offer:
            self.game_manager.commerce_manager.trade_with_player(trade_offer)
        return

    def start_build_phase(self, player=-1):
        """
        Esta función permite pasar a la fase de construcción
        :param player: número que representa al jugador
        :return: void
        """
        print('start build phase: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(2)
        # TODO: Necesita hacer una comprobación que le llega el objeto esperado y no otra cosa
        to_build = self.game_manager.bot_manager.actualPlayer.on_build_phase()
        if to_build:
            built = False
            if to_build[0] == "town":
                built = self.game_manager.build_town(self.game_manager.bot_manager.actualPlayer, to_build[1])
            elif to_build[0] == "city":
                built = self.game_manager.build_city(self.game_manager.bot_manager.actualPlayer, to_build[1])
            elif to_build[0] == "road":
                built = self.game_manager.build_road(self.game_manager.bot_manager.actualPlayer, to_build[1])
            elif to_build[0] == "card":
                # TODO
                pass

            if built:
                self.start_build_phase(self.game_manager.bot_manager.actualPlayer)
            else:
                # TODO: Avisar que no se ha podido construir
                pass
        else:
            return

    def end_turn(self, player=-1):
        """
        Esta función permite finalizar el turno
        :param player: número que representa al jugador
        :return: void
        """
        print('start end turn: ' + str(self.game_manager.turn_manager.get_turn()))
        self.game_manager.turn_manager.set_phase(3)
        self.game_manager.bot_manager.actualPlayer.on_turn_end()
        return

    def end_phase(self):
        # TODO
        # Probablemente innecesario
        print('end phase')
        if self.game_manager.turn_manager.phase == 0:
            self.start_commerce_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
        elif self.game_manager.turn_manager.phase == 1:
            self.start_build_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
        elif self.game_manager.turn_manager.phase == 2:
            self.end_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
        elif self.game_manager.turn_manager.phase == 3:
            if self.game_manager.turn_manager.get_whose_turn_is_it() >= 4:
                self.round_end()
            else:
                self.game_manager.turn_manager.set_whose_turn_is_it(
                    self.game_manager.turn_manager.get_whose_turn_is_it() + 1)
                self.start_turn(self.game_manager.turn_manager.whoseTurnIsIt)
        else:
            pass
        return

    # Round #
    def round_start(self):
        """
        Esta función permite comenzar una ronda nueva
        :return:
        """
        print('---------------------')
        print('round start')
        i = 0
        while i < 5:
            self.game_manager.turn_manager.set_turn(self.game_manager.turn_manager.get_turn() + 1)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)

            self.start_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
            self.start_commerce_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
            self.start_build_phase(self.game_manager.turn_manager.get_whose_turn_is_it())
            self.end_turn(self.game_manager.turn_manager.get_whose_turn_is_it())
            i += 1
        self.round_end()
        return

    def round_end(self):
        """
        Esta función permite acabar una ronda empezada
        :return:
        """
        print('round end')
        print('---------------------')
        if self.game_manager.turn_manager.get_round() >= 2:
            # TODO
            return
        else:
            self.game_manager.turn_manager.set_round(self.game_manager.turn_manager.get_round() + 1)
            self.round_start()

        return

    # Game #
    def game_start(self):
        """
        Esta función permite comenzar una partida nueva
        :return:
        """
        print('game start')
        # Se cargan los bots y se inicializa el tablero
        self.game_manager.bot_manager.load_bots()
        self.game_manager.board.__init__()

        # TODO: falta comprobar que en los nodos adyacentes no hayan pueblos tampoco
        #   Falta también que se entreguen los materiales a los jugadores correspondientes
        #   Y que de alguna manera dejen de repartirse los materiales a todas las instancias de la clase en lugar de a 1

        # Se le da paso al primer jugador para que ponga un poblado y una aldea
        i = 1
        while i <= 4:
            self.game_manager.bot_manager.set_actual_player(i)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)
            node_id, road_to = self.game_manager.bot_manager.actualPlayer.on_game_start(self.game_manager.board)

            # TODO: Si no es valido,
            #  repetir el paso "on_game_start" con el bot. En un segundo fallo directamente se le pone por él
            if self.game_manager.board.nodes[node_id]['player'] == 0:
                self.game_manager.board.nodes[node_id]['player'] = self.game_manager.turn_manager.get_whose_turn_is_it()
                # self.game_manager.bot_manager.get_player_from_int(i).\
                # resources.add_material(self.game_manager.board.nodes[node_id]['adjacentTerrain'], 1)
                self.game_manager.bot_manager.get_player_from_int(i).resources.add_material([0, 1, 2, 3, 4], 1)
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner un nodo invalido")

            # TODO: Si no es valido, hacer lo mismo que con el nodo, solo que mirar si se podría pedir solo la carretera
            if (self.game_manager.board.nodes[node_id]['player'] ==
                    self.game_manager.turn_manager.get_whose_turn_is_it()):
                can_build_road = True
                for roads in self.game_manager.board.nodes[node_id]['roads']:
                    if road_to == roads['NodeID']:
                        can_build_road = False
                        break

                if can_build_road:
                    self.game_manager.board.nodes[node_id]['roads'].append(
                        {
                            "playerID": self.game_manager.turn_manager.get_whose_turn_is_it(),
                            "nodeID": road_to,
                        })
                else:
                    print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                          " ha intentado poner una carretera invalida")

            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner una carretera en un nodo que no le pertence")
            i += 1

        i = 4
        while i >= 1:
            self.game_manager.bot_manager.set_actual_player(i)
            self.game_manager.turn_manager.set_whose_turn_is_it(i)
            node_id, road_to = self.game_manager.bot_manager.actualPlayer.on_game_start(self.game_manager.board)

            # TODO: Si no es valido,
            #  repetir el paso "on_game_start" con el bot. En un segundo fallo directamente se le pone por él
            if self.game_manager.board.nodes[node_id]['player'] == 0:
                self.game_manager.board.nodes[node_id]['player'] = self.game_manager.turn_manager.get_whose_turn_is_it()
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner un nodo invalido")
            # TODO: Si no es valido, hacer lo mismo que con el nodo, solo que mirar si se podría pedir solo la carretera
            if self.game_manager.board.nodes[node_id][
                'player'] == self.game_manager.turn_manager.get_whose_turn_is_it():
                can_build_road = True
                for roads in self.game_manager.board.nodes[node_id]['roads']:
                    if road_to == roads['nodeID']:
                        can_build_road = False
                        break

                if can_build_road:
                    self.game_manager.board.nodes[node_id]['roads'].append(
                        {
                            "playerID": self.game_manager.turn_manager.get_whose_turn_is_it(),
                            "nodeID": road_to,
                        })
                else:
                    print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                          " ha intentado poner una carretera invalida")
            else:
                print("el jugador " + str(self.game_manager.turn_manager.get_whose_turn_is_it()) +
                      " ha intentado poner una carretera en un nodo que no le pertence")
            i -= 1

        ######################################################
        print('Nodos:')
        n = 0
        while n < 54:
            print('ID: ' + str(self.game_manager.board.nodes[n]['id']))
            print('Player: ' + str(self.game_manager.board.nodes[n]['player']))
            print('Roads: ')
            print(self.game_manager.board.nodes[n]['roads'])
            print('---------------------\n')

            n += 1
        ######################################################

        self.round_start()
        return

    def game_end(self):
        """
        Esta función permite acabar una partida empezada
        :return:
        """
        print('game end')
        return

    def check_for_victory(self):
        """
        Esta función comprueba si alguno de los 4 jugadores ha conseguido la condición de victoria
        :return:
        """
        print('check for victory')
        return


if __name__ == '__main__':
    print('#############################')
    GameDirector().game_start()
    print('#############################')
