from move_to import *

def vehn(amount, BASE = (4,4), substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes)-1), iterations = 300):
	#Geometry tables:
	#Opposite dir
	OPP = {
		North: South,
		South: North,
		East: West,
		West: East
	}
	#Change in X when goin dir
	DX = {
		North: 0,
		South: 0,
		East: 1,
		West: -1
	}
	#Change in Y when goin dir
	DY = {
		North: 1,
		South: -1,
		East: 0,
		West: 0
	}

	#Mapping info:
	WALLS = {}
	DIST_TO_BASE = {BASE: 0}
	DIR_TO_BASE = {BASE: None}
	TREASURE_POS = []

	#recursivelly finding walls and the treasure. This is a DFS, or depth-first search method:
	def scan_maze(back=None):
		if get_entity_type() == Entities.Treasure:
			#if there's treasure, mark the position:
			TREASURE_POS.append((get_pos_x(),get_pos_y()))
		WALLS[(get_pos_x(),get_pos_y())] = set()
		for dir in [North,East,South,West]:
			if dir != back:
				if move(dir):
					#if we can move in that direction, call this same function with back = the opposit of what direction we moved.
					scan_maze(OPP[dir])
					move(OPP[dir])
				else:
					#if we can't move, add that direction to walls using current position as keys.
					WALLS[(get_pos_x(),get_pos_y())].add(dir)
	
	#this will update the distance and directions to "BASE" every time we call it.
	def do_bfs(x,y):
		queue = [(x, y, DIST_TO_BASE[x, y])]
		#do this while there's still something at queue
		while queue:
			#get the first element out of queue, which will eventually end the loop.
			old_x, old_y, dist = queue.pop(0)
			#for each direction
			for dir in [North,East,South,West]:
				#if there isn't a wall there
				if dir not in WALLS[old_x,old_y]:
					#check the next step
					new_x = old_x + DX[dir]
					new_y = old_y + DY[dir]
					#if it isn't in DIST_TO_BASE, or it's further from BASE than what was expected (meaning a wall broke)
					if((new_x, new_y) not in DIST_TO_BASE
							or DIST_TO_BASE[new_x, new_y] > dist + 1):
						#Update the variables
						DIST_TO_BASE[new_x, new_y] = dist+1
						DIR_TO_BASE[new_x, new_y] = OPP[dir]
						queue.append((new_x, new_y, dist+1))
	
	# this function will go through the DIR_TO_BASE dictionary directions, starting with the keys at your position
	# and return a list of ordered directions you have to take to get to "BASE"
	def get_path_to_base(x=get_pos_x(), y=get_pos_y()):
		path = []
		dir = DIR_TO_BASE[x,y]
		while dir:
			path.append(dir)
			x += DX[dir]
			y += DY[dir]
			dir = DIR_TO_BASE[x, y]
		return path
	
	#this function will attempt to move in every direction on each step, mapping destroyed walls:
	def move_and_break_walls(step):
		move(step)
		# For each direction in WALLS for the current position:
		for dir in list(WALLS[get_pos_x(), get_pos_y()]):
			# Try to move in that direction:
			if move(dir):
				# If successfull, we'll update the walls on both sides.
				# First, get the position we just moved to:
				new_x = get_pos_x()
				new_y = get_pos_y()
				# Move back:
				move(OPP[dir])
				# Remove both sides
				WALLS[get_pos_x(), get_pos_y()].remove(dir)
				WALLS[new_x, new_y].remove(OPP[dir])
				# Update the flowfield from both positions:
				do_bfs(get_pos_x(), get_pos_y())
				do_bfs(new_x, new_y)

	#Map the maze:
	scan_maze()
	do_bfs(BASE[0],BASE[1])

	#First solve of the maze is simple, since we're back at "BASE":
	#If there's no treasure
	if get_entity_type() != Entities.Treasure:
		#Get the treasure position:
		x,y = TREASURE_POS[0]
		#Get the path to base from the treasure:
		gpath = get_path_to_base(x, y)
		for step in gpath[::-1]:
			# Since the path is from the treasure to base, we move on opposite directions:
			move(OPP[step])

	#Solve and recicle the maze many times:
	for _ in range(iterations-1):
		#where's the next treasure?
		gx, gy = measure()
		# Compute paths from drone and treasure to base:
		dpath = get_path_to_base()
		gpath = get_path_to_base(gx, gy)

		# Recycle the treasure if it's here
		use_item(Items.Weird_Substance,substance)
		
		# This will cancel moves that are the same, making sure we don't have to always get back to the "BASE"
		# If the treasure is closer to us
		while dpath and gpath and dpath[-1] == gpath[-1]:
			gpath.pop()
			dpath.pop()

		# Move the drone foward towards "base", up to where the drone and treasure share a corner:
		for step in dpath:
			move_and_break_walls(step)
		# Move the drone "backwards" towards the treasure:
		for step in gpath[::-1]:
			move_and_break_walls(OPP[step])
		
		#if we've got enough gold, don't do 300 iterations:
		if num_items(Items.Gold) >= amount:
			break
	#harvest the last treasure instead of reciclying it:
	harvest()