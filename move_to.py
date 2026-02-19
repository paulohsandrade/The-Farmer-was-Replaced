def move_to(goal_x, goal_y, current_x = get_pos_x(), current_y = get_pos_y(), ws = get_world_size()):
	hws = ws // 2
	# Calculate the shortest x direction
	dx = (goal_x - current_x + hws) % ws - hws
	# Calculate the shortest y direction
	dy = (goal_y - current_y + hws) % ws - hws

	# Move in x direction
	for _ in range(dx):
		move(East)
	for _ in range(-dx):
		move(West)

	# Move in y direction
	for _ in range(dy):
		move(North)
	for _ in range(-dy):
		move(South)

def move_to_list(goal):
	goal_x = goal[0]
	goal_y = goal[1]
	ws = get_world_size()
	current_y = get_pos_y()
	current_x = get_pos_x()
	hws = ws // 2
	# Calculate the shortest x direction
	dx = (goal_x - current_x + hws) % ws - hws
	# Calculate the shortest y direction
	dy = (goal_y - current_y + hws) % ws - hws

	# Move in x direction
	for _ in range(dx):
		move(East)
	for _ in range(-dx):
		move(West)

	# Move in y direction
	for _ in range(dy):
		move(North)
	for _ in range(-dy):
		move(South)

def move_to_pos(goal_pos, current_pos, ws = get_world_size()):
	hws = ws // 2
	goal_x, goal_y = goal_pos
	start_x, start_y = current_pos

	dx = (goal_x - start_x + hws) % ws - hws
	dy = (goal_y - start_y + hws) % ws - hws

	for i in range(dx):
		move(East)
	for i in range(-dx):
		move(West)
	for i in range(dy):
		move(North)
	for i in range(-dy):
		move(South)