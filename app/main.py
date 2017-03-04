import bottle
import os
import random

spiraling = 0
spiral_focus = {None,None}

@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
	data = bottle.request.json
	game_id = data['game_id']
	board_width = data['width']
	board_height = data['height']

	head_url = '%s://%s/static/head.png' % (
		bottle.request.urlparts.scheme,
		bottle.request.urlparts.netloc
	)

	# TODO: Do things with data

	return {
		'color': '#00FF00',
		'taunt': 'taunt'.format(game_id, board_width, board_height),
		'head_url': head_url,
		'name': '[insert name here]'
	}

def checkSpace(x,y,data,board):
	if x >= data['width'] or y >= data['height']:
		return 0
	if board[x][y] == 2 or board[x][y] == 3 or board[x][y] == 4:
		return 0
	else:
		return 1

def seeTheFuture(board,data,turns):
	if turns < 1:
		return board
	newBoard = list(board)
	for i in range(data['width']):
		for k in range(data['height']):
			if x == 2:
				newBoard[x-1][i] = 2
				newBoard[x+1][i] = 2
				newBoard[x][i-1] = 2
				newBoard[x][i+1] = 2
	return seeTheFuture(newBoard,data,turns-1)
				
def spiral(x,y,myself,data,board):
	seeTheFuture(board,data,4)
	if size <= 7:
		future = seeTheFuture(board,data,4)
		if future[x][y] == 2:
			return
		if myself['coords'][0] < x and myself['coords'][0] < y:
			return
	elif size <= 15:
		return
	
	elif size > 15:
		return


@bottle.post('/move')
def move():
	data = bottle.request.json
	board = [[0 for x in range(data['width'])]for y in range(data['height'])]
	
	
	#if spiraling == 1:
		#return spiral(spiral_focus[0],spiral_focus[1],)

	# TODO: Do things with data
	directions = ['up', 'down', 'left', 'right']

	for enemy in data['snakes']:
		if (enemy['id'] == ID):
			myself = enemy;
			for space in enemy['coords'][2:-1]:
				board[space[0]][space[1]] = 3
	   		board[enemy['coords'][0]][enemy['coords'][1]] = 4
			continue
		board[enemy['coords'][0]][enemy['coords'][1]] = 2
		for space in enemy['coords'][2:-1]:
			board[space[0]][space[1]] = 3
		board[enemy['coords'][0]][enemy['coords'][1]] = 4
	
	direction = random.choice(directions)
	if direction == 'up':
		go = {myself['coords'][0],myself['coords'][1]-1}
	elif direction == 'down':
		go = {myself['coords'][0],myself['coords'][1]+1}
	elif direction == 'left':
		go = {myself['coords'][0]-1,myself['coords'][1]}
	elif direction == 'right':
		go = {myself['coords'][0]+1,myself['coords'][1]}
		
	while not checkSpace(myself['coords'][0],myself['coords'][1],data,board):
		direction = random.choice(directions)
	if direction == 'up':
		go = {myself['coords'][0],myself['coords'][1]-1}
	elif direction == 'down':
		go = {myself['coords'][0],myself['coords'][1]+1}
	elif direction == 'left':
		go = {myself['coords'][0]-1,myself['coords'][1]}
	elif direction == 'right':
		go = {myself['coords'][0]+1,myself['coords'][1]}
	
	return {
		'move': direction,
		'taunt': '???'
	}


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
	bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
