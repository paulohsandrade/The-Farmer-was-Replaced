from move_to import *

def sort_row():
	n = get_world_size()
	y = get_pos_y()

	# Go to the left end once (x=0) to make the indexing consistent
	while get_pos_x() != 0:
		move(West)

	low = 0
	high = n - 1

	while low < high:
		changed = False

		# ---- Left -> Right pass ----
		# Move to low (usually already there after the right->left pass)
		while get_pos_x() < low:
			move(East)
		while get_pos_x() > low:
			move(West)

		last_swap = low
		# Scan to high, swapping (x, x+1) if out of order
		while get_pos_x() < high:
			if measure() > measure(East):
				swap(East)
				changed = True
				last_swap = get_pos_x()
			move(East)

		# Everything to the right of last_swap is now settled
		high = last_swap
		if not changed or low >= high:
			break
		
		# Tiny window break:
		if high - low <= 1:			 
			break

		changed = False

		# ---- Right -> Left pass ----
		# We're already at x == previous high end from the scan above.
		last_swap = high
		while get_pos_x() > low:
			# Compare (x-1, x) using West neighbor
			if measure(West) > measure():
				swap(West)
				changed = True
				last_swap = get_pos_x() - 1  # left index of swapped pair
			move(West)

		# Everything to the left of last_swap is now settled
		low = last_swap
		if not changed:
			break

		# Tiny window break:
		if high - low <= 1:			 
			break

def plant_row(row):
	def task():
		move_to(0,row)
		n = get_world_size()

		for col in range(n):
			if get_ground_type() == Grounds.Grassland:
				till()
			plant(Entities.Cactus)

			if get_pos_x() > 0 and measure() < measure(West):
				swap(West)
			move(East)
		sort_row()
	return task

# Doing that in parallel with maximum ammount of drones
def plant_all_rows():
	n = get_world_size()
	handles = []
	row = 0
	while row < n:
		for drone in range(max_drones()-1):
			h = spawn_drone(plant_row(row))
			handles.append(h)
			row += 1
			if row >= n-1:
				break
		plant_row(row)()
		row += 1
		for h in handles:
			wait_for(h)
		handles = []

# Doing that in parallel with maximum ammount of drones
# def sort_all_rows():
# 	n = get_world_size()
# 	handles = []

# 	for row in range(n):
# 		move_to(0, row)

# 		if num_drones() < max_drones():
# 			h = spawn_drone(sort_row)
# 			handles.append(h)
# 		else:
# 			sort_row()

# 	for h in handles:
# 		if h != None:
# 			wait_for(h)

def sort_col(col):
	def task():
		move_to(col,0)
		n = get_world_size()
		x = get_pos_x()

		# Go to the left end once (x=0) to make the indexing consistent
		while get_pos_y() != 0:
			move(South)

		low = 0
		high = n - 1

		while low < high:
			changed = False

			# ---- Left -> Right pass ----
			# Move to low (usually already there after the right->left pass)
			while get_pos_y() < low:
				move(North)
			while get_pos_y() > low:
				move(South)

			last_swap = low
			# Scan to high, swapping (x, x+1) if out of order
			while get_pos_y() < high:
				if measure() > measure(North):
					swap(North)
					changed = True
					last_swap = get_pos_y()
				move(North)

			# Everything to the right of last_swap is now settled
			high = last_swap
			if not changed or low >= high:
				break

			# Tiny window break:
			if high - low <= 1:			 
				break

			changed = False

			# ---- Right -> Left pass ----
			# We're already at x == previous high end from the scan above.
			last_swap = high
			while get_pos_y() > low:
				# Compare (x-1, x) using West neighbor
				if measure(South) > measure():
					swap(South)
					changed = True
					last_swap = get_pos_y() - 1  # left index of swapped pair
				move(South)

			# Everything to the left of last_swap is now settled
			low = last_swap
			if not changed:
				break

			# Tiny window break:
			if high - low <= 1:			 
				break
	return task

# Doing that in parallel with maximum ammount of drones
def sort_all_cols():
	n = get_world_size()
	handles = []
	col = 0
	while col < n:
		for drone in range(max_drones()-1):
			h = spawn_drone(sort_col(col))
			handles.append(h)
			col += 1
			if col >= n-1:
				break
		sort_col(col)()
		col += 1
		for h in handles:
			wait_for(h)
		handles = []

# Run untill you have "amount" cacti
def multi_drones_cacti(amount):
	while num_items(Items.Cactus) < amount:

		plant_all_rows() 
		#sort_all_rows()
		sort_all_cols()

		harvest()

#multi_drones_cacti(33554432)
