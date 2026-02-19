import move_to

def plant_and_sort_row():
	n = get_world_size()

	for col in range(n):
		# Plant
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Cactus)

		# Sort last planted
		left = 0
		while left < col and measure() < measure(West):
			swap(West)
			move(West)
			left += 1

		if left > 0:
			move_to.move_to(col,get_pos_y())
		move(East)

# Doing that in parallel with maximum ammount of drones
def plant_and_sort_all_rows():
	n = get_world_size()
	handles = []

	for row in range(n):
		move_to.move_to(0, row)

		if num_drones() < max_drones():
			h = spawn_drone(plant_and_sort_row)
			handles.append(h)
		else:
			plant_and_sort_row()

	for h in handles:
		if h != None:
			wait_for(h)

# Same logic, but no planting needed
def sort_col():
	n = get_world_size()

	for row in range(n):
		down = 0
		while down < row and measure() < measure(South):
			swap(South)
			move(South)
			down += 1

		if down > 0:
			move_to.move_to(get_pos_x(),row)
		move(North)

def sort_all_cols():
	n = get_world_size()
	handles = []

	for col in range(n):
		move_to.move_to(col, 0)

		if num_drones() < max_drones():
			h = spawn_drone(sort_col)
			handles.append(h)
		else:
			sort_col()

	for h in handles:
		if h != None:
			wait_for(h)

# Run untill you have "amount" cacti
def multi_drones_cacti(amount):
	while num_items(Items.Cactus) < amount:
		move_to.move_to(0, 0)

		plant_and_sort_all_rows() 
		sort_all_cols()

		harvest()
