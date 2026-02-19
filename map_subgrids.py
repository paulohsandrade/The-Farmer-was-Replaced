
def generate_moves_quadrant(gsx,gsy):
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

def generate_quadrant_coords(gsx,gsy,ws = get_world_size(), md = max_drones()):
	coords = list()
	coords.append((0,0))
	if md == 2 and gsx >= gsy:
		coords.append((0,ws/2))
	elif md == 2 and gsx < gsy:
		coords.append((ws/2,0))
	if md == 4:
		coords.append((0,ws/2))
		coords.append((ws/2,ws/2))
		coords.append((ws/2,0))
	if md == 8 and gsx >= gsy:
		coords.append((0,ws/4))
		coords.append((0,ws/2))
		coords.append((0,ws*3/4))
		coords.append((ws/2,ws*3/4))
		coords.append((ws/2,ws/2))
		coords.append((ws/2,ws/4))
		coords.append((ws/2,0))
	if md == 8 and gsx < gsy:
		coords.append((ws/4,0))
		coords.append((ws/2,0))
		coords.append((ws*3/4,0))
		coords.append((ws*3/4,ws/2))
		coords.append((ws/2,ws/2))
		coords.append((ws/4,ws/2))
		coords.append((0,ws/2))
	if md == 16:
		coords.append((0,ws/4))
		coords.append((0,ws/2))
		coords.append((0,ws*3/4))
		coords.append((ws/4,0))
		coords.append((ws/4,ws/4))
		coords.append((ws/4,ws/2))
		coords.append((ws/4,ws*3/4))
		coords.append((ws/2,0))
		coords.append((ws/2,ws/4))
		coords.append((ws/2,ws/2))
		coords.append((ws/2,ws*3/4))
		coords.append((ws*3/4,0))
		coords.append((ws*3/4,ws/4))
		coords.append((ws*3/4,ws/2))
		coords.append((ws*3/4,ws*3/4))
	return coords


#testing stuff:
# def task_wrapper(MOVES):
# 	def task():
# 		while True:
# 			for dir in MOVES:
# 				till()
# 				move(dir)
# 	return task

# set_execution_speed(2)
# set_world_size(12)
# ws = get_world_size()
# md = 8
# from move_to import move_to
# MOVES = generate_moves_quadrant(3,6)
# COORDS = generate_quadrant_coords(3,6,ws,md)
# quick_print(COORDS)
# drones = []
# for _ in range(len(COORDS)-1):
# 	move_to(COORDS[_][0],COORDS[_][1])
# 	drones.append(spawn_drone(task_wrapper(MOVES)))
# move_to(COORDS[_+1][0],COORDS[_+1][1])
# task_wrapper(MOVES)()