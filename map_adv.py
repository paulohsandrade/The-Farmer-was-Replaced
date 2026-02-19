def generate_moves(
		n = get_world_size()**2,
		world_size = get_world_size(),
		pos_x = 0,
		pos_y = 0
	):
	moves = []
	if n > world_size**2:
		world_moves = generate_moves(world_size**2, world_size, pos_x, pos_y)
		for i in range(n // world_size**2):
			moves += world_moves
		n %= world_size**2

	for i in range(n):
		if pos_x % world_size == pos_y % world_size:
			pos_x -= 1
			moves.append(West)
		else:
			pos_y += 1
			moves.append(North)
	return moves

def generate_moves_reversed(
		n = get_world_size()**2,
		world_size = get_world_size(),
		pos_x = 0,
		pos_y = 0
	):
	moves = []
	if n > world_size**2:
		world_moves = generate_moves(world_size**2, world_size, pos_x, pos_y)
		for i in range(n // world_size**2):
			moves += world_moves
		n %= world_size**2

	for i in range(n):
		if pos_x % world_size == pos_y % world_size:
			pos_x -= 1
			moves.append(East)
		else:
			pos_y += 1
			moves.append(South)
	return moves

def generate_moves_pos(ws=get_world_size(),pos_x = 0,pos_y = 0):
	moves = []
	rr1 = range(ws)
	rr2 = range(ws-1)
	for x in rr1:
		for y in rr2:
			moves.append((North, (pos_x, pos_y)))
			pos_y = (pos_y + 1) % ws
		moves.append((East, (pos_x, pos_y)))
		pos_x = (pos_x + 1) % ws
	return moves