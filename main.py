import os
import cherrypy
from best_move import best
"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            'color': '#888888',
            'author': 'DAChenScratch',
            'apiversion':"1",
            'version':'1.00',
            "head":"default",
            "tail":"default",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        data = cherrypy.request.json
        #easy heuristic tuning
        scores = [
          350, 1.5, 70, 1.3, 60, 60, 60, 70, 55, 2.5, 60
        ]
        for snake in data['board']['snakes']:
          print(snake['name'], 'says:', snake['shout'])
        print(f"TURN NUMBER: {data['turn']}")
        move = best(data, scores)
        print('Sending move response as:', {"move": move})
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        data = cherrypy.request.json
        names = 'Snake names are: '
        for snake in data['board']['snakes']:
          if data['board']['snakes'].index(snake) != len(data['board']['snakes']) - 1:
            names =  names + snake['name'] + ', '
          else:
            if not len(data['board']['snakes']) == 1:
              names = names + 'and ' + snake['name'] + '.'
            else:
              names = names  + snake['name'] + '.'
        #os.system('clear')
        print('SNAKES REMAINING:', len(data['board']['snakes']))
        print(names)
        if len(data['board']['snakes']) == 1 and names == 'Snake names are: ' + data['you']['name']+'.':
          print('YEAH!!! VICTORY!!!')
        else:
          print('\n\n\n\nF in the terminal I lost.')
        return "hi"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)