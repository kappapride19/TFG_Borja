from Managers.GameDirector import GameDirector


def main():
    games_changing_bots = str(input('Iniciar simulación con estrategias evolutivas (y/n): '))
    if games_changing_bots=='n':
        game_director = GameDirector()
        try:
            games_to_play = int(input('Cantidad de partidas a jugar: '))
        except ValueError:
            games_to_play = 0
        if isinstance(games_to_play, int) and games_to_play > 0:
            for i in range(games_to_play):
                print('......')
                game_director.game_start(i + 1)
        else:
            print('......')
            print('Cantidad no válida')
        print('------------------------')
        game_director.trace_loader.export_every_game_to_file()
        return
    elif games_changing_bots == 'y':
        game_director = GameDirector(for_advanced=True)
        try:
            games_to_play = int(input('Cantidad de partidas a jugar: '))
        except ValueError:
            games_to_play = 0
        if isinstance(games_to_play, int) and games_to_play > 0:
            for i in range(games_to_play):
                print('......')
                game_director.game_start(i + 1,True)
        else:
            print('......')
            print('Cantidad no válida')
        print('------------------------')
        game_director.trace_loader.export_every_game_to_file()
        return

    else:
        print('Input no válido')
        return


if __name__ == '__main__':
    main()
