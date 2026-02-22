def generate_moves_quadrant(ws = get_world_size(),md = max_drones()):
	nx = 1
	while (nx * 2) * (nx * 2) <= md:
		nx *= 2
	ny = md // nx

	# Quadrant dimensions
	gsx = ws // nx  # width of quadrant
	gsy = ws // ny  # height of quadrant

	
	moves = list()
	if gsx >= gsy:
		k=0
		while len(moves) < (gsx * gsy)-gsx:
			if k == 0:
				for i in range(gsy-1):
					moves.append(North)
			else:
				for i in range(gsy-2):
					moves.append(North)
			moves.append(East)
			for i in range(gsy-2):
				moves.append(South)
			moves.append(East)
			k += 1
		moves.pop()
		moves.append(South)
		for i in range(gsx-1):
			moves.append(West)
	else:
		k=0
		while len(moves) < (gsx * gsy)-gsy:
			if k == 0:
				for i in range(gsx-1):
					moves.append(East)
			else:
				for i in range(gsx-2):
					moves.append(East)
			moves.append(North)
			for i in range(gsx-2):
				moves.append(West)
			moves.append(North)
			k += 1
		moves.pop()
		moves.append(West)
		for i in range(gsy-1):
			moves.append(South)
	return moves

def generate_quadrant_coords(ws=get_world_size(), md=max_drones()):
	# Returns bottom-left (x,y) origins for md subgrids covering a ws x ws world.

	# Assumptions:
	#   - md is a power of two (<= 32)
	#   - ws is one of: 6, 8, 12, 16, 32 (or any ws divisible by the chosen nx, ny)

	# Strategy:
	#   - Choose nx as the largest power of two such that nx*nx <= md
	#   - ny = md // nx
	#   - Tile the world into nx columns and ny rows
	#   - Return coords in a serpentine ("snake") y-order per x-column

	# Find nx = largest power of two where nx*nx <= md
	nx = 1
	while (nx * 2) * (nx * 2) <= md:
		nx *= 2
	ny = md // nx
	gsx = ws // nx
	gsy = ws // ny

	coords = []
	for ix in range(nx):
		# Snake ordering in y
		if ix % 2 == 0:
			y_range = range(ny)			   # 0..ny-1
		else:
			y_range = range(ny - 1, -1, -1)   # ny-1..0

		x0 = ix * gsx
		for iy in y_range:
			y0 = iy * gsy
			coords.append((x0, y0))

	return coords

