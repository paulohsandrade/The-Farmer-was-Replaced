from move_to import *
import queue_utils
import heartbeat
# import skyscraper
# import hilbert
# import starburst

def dinos(amount):
	#set_world_size(12)

	# geometry:
	OPP = {North: South, East: West,
		South: North, West: East}

	# auxiliary:
	path_ids = {}
	current_cycle_length = 0
	full_cycle_length = get_world_size()**2
	current_tail_length = 1
	next_apple = (0,0)
	last_dir = None

	# --- NEW: early-game "go straight to the apple" length threshold ---
	CHASE_LEN = full_cycle_length // 6   # tune: //8 more aggressive, //12 safer
	if CHASE_LEN < 6:
		CHASE_LEN = 6

	def prep():
		move_to(0,0)
		# if get_world_size() == 16 or get_world_size() == 32:
		# 	hilbert.gen_hilbert_path(path_ids)
		# else:
		# 	heartbeat.gen_heartbeat_path(path_ids)
		heartbeat.gen_heartbeat_path(path_ids)

	def scoot(dir, sc):
		global current_tail_length
		global current_cycle_length
		global next_apple

		move(dir)
		here = (get_pos_x(), get_pos_y())
		current_cycle_length -= sc
		queue_utils.tpush((here, sc))

		if(here == next_apple):
			current_tail_length += 1
			next_apple = measure()
			return True
		else:
			tail = queue_utils.tpop()
			current_cycle_length += tail[1]
			return False

	def get_tgt(here, dir):
		if dir == North:
			return (here[0],here[1]+1)
		if dir == East:
			return (here[0]+1, here[1])
		if dir == South:
			return (here[0],here[1]-1)
		if dir == West:
			return (here[0]-1,here[1])
		return here

	def mod_between(tgt, start, end, mod):
		if(end < start):
			end += mod
		if(tgt < start):
			tgt += mod
		return (tgt >= start and tgt <= end)

	def can_shortcut(here, dir, here_idx, tail_idx, apple_idx):
		global current_cycle_length
		global current_tail_length
		global full_cycle_length

		if not can_move(dir):
			return 0

		tgt = get_tgt(here, dir)
		tgt_idx = path_ids[tgt][0]

		# Don't get ahead of my tail
		if(mod_between(tgt_idx,tail_idx,here_idx,full_cycle_length)):
			return 0

		# Don't skip past the apple
		if(not mod_between(tgt_idx,here_idx,apple_idx,full_cycle_length)):
			return 0

		if(tgt_idx < here_idx):
			tgt_idx += full_cycle_length
		# less 1 because moving from n -> n+1 shortens the len by 0, not 1
		removed_len = tgt_idx - here_idx - 1

		# arbitrary +1 in case of apples on the return path
		if current_cycle_length - removed_len > current_tail_length + 1:
			return removed_len
		else:
			return 0

	# --- NEW: weaker legality check for "chase apple" mode ---
	def can_step_legal(here, dir, here_idx, tail_idx, apple_idx):
		global full_cycle_length

		if not can_move(dir):
			return False

		tgt = get_tgt(here, dir)
		tgt_idx = path_ids[tgt][0]

		# Don't get ahead of tail (cycle-order collision risk)
		if mod_between(tgt_idx, tail_idx, here_idx, full_cycle_length):
			return False

		# Don't skip past the apple in cycle order
		if not mod_between(tgt_idx, here_idx, apple_idx, full_cycle_length):
			return False

		return True

	# --- NEW: chase ordering (Y toward apple first, then X) ---
	def chase_dirs(here, apple, go_dir, last_dir_local):
		global OPP

		avoid1 = go_dir
		if last_dir_local != None:
			avoid2 = OPP[last_dir_local]
		else:
			avoid2 = None

		hx, hy = here
		ax, ay = apple

		y_dir = None
		if ay > hy:
			y_dir = North
		elif ay < hy:
			y_dir = South

		x_dir = None
		if ax > hx:
			x_dir = East
		elif ax < hx:
			x_dir = West

		order = []
		if y_dir != None:
			order.append(y_dir)
		if x_dir != None:
			order.append(x_dir)

		# Fill remaining dirs in a fixed order
		for d in [North, East, South, West]:
			dup = False
			for e in order:
				if e == d:
					dup = True
					break
			if not dup:
				order.append(d)

		# Filter out go_dir and reverse(last_dir)
		out = []
		for d in order:
			if d == avoid1 or d == avoid2:
				continue
			dup = False
			for e in out:
				if e == d:
					dup = True
					break
			if not dup:
				out.append(d)

		return out

	def build_wanna_dirs(here, apple, go_dir, last_dir_local):
		global OPP
		# Exclude: go_dir (fallback) and reverse of last_dir (immediate collision)
		avoid1 = go_dir
		if last_dir_local != None:
			avoid2 = OPP[last_dir_local]
		else:
			avoid2 = None

		hx, hy = here
		ax, ay = apple

		dx = ax - hx
		dy = ay - hy
		if dx < 0:
			dx = -dx
		if dy < 0:
			dy = -dy

		# Preferred direction on each axis (no torus)
		if ax > hx:
			x_pref = East
		elif ax < hx:
			x_pref = West
		else:
			x_pref = None

		if ay > hy:
			y_pref = North
		elif ay < hy:
			y_pref = South
		else:
			y_pref = None

		# Secondary (opposite) directions
		if x_pref != None:
			x_alt = OPP[x_pref]
		else:
			x_alt = None
		if y_pref != None:
			y_alt = OPP[y_pref]
		else:
			y_alt = None

		# Assemble candidates in priority order: larger axis first
		dirs = []

		if dx >= dy:
			if x_pref != None:
				dirs.append(x_pref)
			if y_pref != None:
				dirs.append(y_pref)
			if y_alt != None:
				dirs.append(y_alt)
			if x_alt != None:
				dirs.append(x_alt)
		else:
			if y_pref != None:
				dirs.append(y_pref)
			if x_pref != None:
				dirs.append(x_pref)
			if x_alt != None:
				dirs.append(x_alt)
			if y_alt != None:
				dirs.append(y_alt)

		# Filter out duplicates + avoid dirs, preserve order
		out = []
		for d in dirs:
			if d == None:
				continue
			if d == avoid1 or d == avoid2:
				continue
			dup = False
			for e in out:
				if e == d:
					dup = True
					break
			if not dup:
				out.append(d)

		return out

	def dino_iter():
		global current_tail_length
		global full_cycle_length
		global last_dir

		here = (get_pos_x(), get_pos_y())
		go_dir = path_ids[here][1]
		go_saves = 0

		# If we're covering more than 1/4 the board, just follow the Hamiltonian path
		if (current_tail_length >= full_cycle_length*1/4):
			last_dir = go_dir
			return scoot(go_dir, go_saves)

		# Heartbeat "fastlane" heuristic
		fave_dir = None
		Z = get_world_size()

		if (here[1] > Z/2 and (next_apple[1] < Z/2 or next_apple[0] < here[0])):
			fave_dir = South

		if (here[1] < Z/2-1 and (next_apple[1] >= Z/2 or next_apple[0] > here[0])):
			fave_dir = North

		tail = queue_utils.tpeek()
		tail_loc = tail[0]

		here_idx = path_ids[here][0]
		tail_idx = path_ids[tail_loc][0]
		apple_idx = path_ids[next_apple][0]

		# ---- NEW: Early game, go straight for the apple (no shortcut math) ----
		if current_tail_length < CHASE_LEN:
			chase = chase_dirs(here, next_apple, go_dir, last_dir)
			for dir in chase:
				if can_step_legal(here, dir, here_idx, tail_idx, apple_idx):
					go_dir = dir
					go_saves = 0
					break
			last_dir = go_dir
			return scoot(go_dir, go_saves)

		# Otherwise, allow shortcutting (your existing behavior)
		wanna_dirs = build_wanna_dirs(here, next_apple, go_dir, last_dir)

		if (not go_dir == fave_dir):
			for dir in wanna_dirs:
				this_saves = can_shortcut(here, dir, here_idx, tail_idx, apple_idx)
				if (this_saves > go_saves):
					go_dir = dir
					go_saves = this_saves
					# stops after finding the first shortcut:
					break

		last_dir = go_dir
		return scoot(go_dir, go_saves)

	def dino_goto():
		while(not dino_iter()):
			continue

	def farm():
		global full_cycle_length
		global current_tail_length
		global current_cycle_length
		global next_apple

		queue_utils.reset()
		move_to(0,0)
		change_hat(Hats.Dinosaur_Hat)

		current_tail_length = 1
		current_cycle_length = full_cycle_length
		next_apple = measure()
		queue_utils.tpush(((0,0),0))

		start = get_time()

		while (current_tail_length < full_cycle_length - 1):
			dino_goto()
		clear()

	prep()
	while num_items(Items.Bone) < amount:
		farm()

#set_world_size(12)
#dinos(10000000000000000000000000)