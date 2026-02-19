import timing

def try_ulock(upgrade,num,last_time):
	time = get_time()
	time_diff = timing.time_difference(last_time,time)
	str_time = timing.time_units(time)
	
	if unlock(upgrade):
		success = "Successfully Unlocked "+str(upgrade)+" "+str(num)
		return_string = success + " || " + "at " + str_time + " || " + time_diff + " since last"
		return return_string, time
	
	else:
		failure = "Failed to Unlocked "+str(upgrade)+" "+str(num)
		return_string = failure + " || " + "at " + str_time + " || " + time_diff + " since last"
		return return_string, time

unlock_levels = {
	Unlocks.Cactus: 0,
	Unlocks.Carrots: 0,
	Unlocks.Dinosaurs: 0,
	Unlocks.Expand: 0,
	Unlocks.Fertilizer: 0,
	Unlocks.Grass: 0,
	Unlocks.Mazes: 0,
	Unlocks.Megafarm: 0,
	Unlocks.Plant: 0,
	Unlocks.Polyculture: 0,
	Unlocks.Pumpkins: 0,
	Unlocks.Speed: 0,
	Unlocks.Sunflowers: 0,
	Unlocks.Trees: 0,
	Unlocks.Watering: 0
}

#farm 100 for:
	# 0 : 11.14 || Unlocks.Speed 1 -> Hay 20
	# 0 : 36.49 || Unlocks.Plant 1 -> Hay 50
	# 0 : 51.77 || Unlocks.Expand 1 -> Hay 30
# 1 : 39.05 || Unlocks.Expand 2 -> Wood 20
# 2 : 4.51 || Unlocks.Speed 2 -> Wood 20
# 3 : 29.91 || Unlocks.Carrots 1 -> Wood: 50
# 3 : 35.74 || Unlocks.Grass 2 -> Hay: 300
#farm for:
	# 4 : 54.22 || Unlocks.Trees 1 -> Wood: 50, Carrot: 70
	# 4 : 54.45 || Unlocks.Trees 2 -> Hay: 300
# 5 : 13.85 || Unlocks.Expand 3 -> Wood 30, Carrot 20
# 5 : 44.98 || Unlocks.Carrots 2 -> Wood: 250
# 5 : 59.61 || Unlocks.Speed 3 -> Wood 50, Carrot 50
#farm for:
	# 6 : 20.07 || Unlocks.Expand 4 -> Wood 100, Carrot 50
	# 6 : 20.69 || Unlocks.Watering 1 -> Wood: 50
	# 6 : 21.16 || Unlocks.Watering 2 -> Wood: 200
# 7 : 29.06 || Unlocks.Carrots 3 -> Wood: 1250
# 8 : 2.91 || Unlocks.Grass 3 -> Wood: 500
# 8 : 32.56 || Unlocks.Sunflowers 1 -> Carrot: 500
# 9 : 2.66 || Unlocks.Fertilizer 1 -> Wood: 500
# 9 : 30.3 || Unlocks.Watering 3 -> Wood: 800
# 9 : 34.47 || Unlocks.Speed 4 -> Carrot 500
#farm for:
	# 11 : 15.57 || Unlocks.Pumpkins 1 -> Wood: 500, Carrot: 200
	# 11 : 15.63 || Unlocks.Watering 4 -> Wood: 3200
# 13 : 16.26 || Unlocks.Polyculture 1 -> Pumpkin: 3000
# 13 : 33.76 || Unlocks.Speed 5 -> Carrot 1000
# 14 : 11.71 || Unlocks.Expand 5 -> Pumpkin 1000
# 14 : 18.26 || Unlocks.Fertilizer 2 -> Wood: 1500
# 14 : 18.3 || Unlocks.Mazes 1 -> Weird_Substance: 1000
# 14 : 38.89 || Unlocks.Megafarm 1 -> Gold: 2000
#farm for:
	# 15 : 18.02 || Unlocks.Trees 3 -> Hay: 1200 
	# 15 : 18.05 || Unlocks.Trees 4 -> Hay: 4800
# 15 : 35.96 || Unlocks.Carrots 4 -> Wood: 6250
# 15 : 51.38 || Unlocks.Watering 5 -> Wood: 12800
#farm for:
	# 16 : 13.86 || Unlocks.Pumpkins 2 -> Carrot: 1000
	# 16 : 13.89 || Unlocks.Pumpkins 3 -> Carrot: 4000
# 17 : 28.09 || Unlocks.Expand 6 -> Pumpkin: 8000
# 18 : 8.5 || Unlocks.Cactus 1 -> Pumpkin: 5000
# 20 : 35.38 || Unlocks.Dinosaurs 1 -> Cactus: 2000
# 20 : 35.41 || Unlocks.Dinosaurs 2 -> Cactus: 12000
# 21 : 19.5 || Unlocks.Polyculture 2 -> Bone: 10000
#farm for:
	# 21 : 19.54 || Unlocks.Mazes 2 -> Cactus: 12000
	# 21 : 19.57 || Unlocks.Mazes 3 -> Cactus: 72000
# 22 : 30.41 || Unlocks.Megafarm 2 -> Gold: 8000
# 22 : 30.45 || Unlocks.Megafarm 3 -> Gold: 32000
# 22 : 30.48 || Unlocks.Grass 4 -> Wood: 2500
# 22 : 40.31 || Unlocks.Trees 5 -> Hay: 19200
#farm for:
	# 22 : 46.94 || Unlocks.Fertilizer 3 -> Wood: 9000
	# 22 : 46.98 || Unlocks.Fertilizer 4 -> Wood: 54000
#farm for:
	# 23 : 4 || Unlocks.Watering 6 -> Wood: 51200
	# 23 : 4.03 || Unlocks.Carrots 5 -> Wood: 31200
# 23 : 15.26 || Unlocks.Carrots 6 -> Wood: 156000
# 23 : 28.02 || Unlocks.Pumpkins 4 -> Carrot: 16000
# 23 : 39.01 || Unlocks.Pumpkins 5 -> Carrot: 64000
# 24 : 2.74 || Unlocks.Expand 7 -> Pumpkin: 64000
# 24 : 54.76 || Unlocks.Megafarm 4 -> Gold: 128000
#farm for:
	# 26 : 4.45 || Unlocks.Cactus 2 -> Pumpkin: 20000
	# 26 : 4.49 || Unlocks.Cactus 3 -> Pumpkin: 120000
#farm for:
	# 26 : 14.27 || Unlocks.Dinosaurs 3 -> Cactus: 72000
	# 26 : 25.24 || Unlocks.Dinosaurs 4 -> Cactus: 432000
	# 28 : 10.96 || Unlocks.Dinosaurs 5 -> Cactus: 2590000
	# 28 : 30.71 || Unlocks.Mazes 4 -> Cactus: 432000
# 33 : 17.56 || Unlocks.Leaderboard 1 -> Bone: 2000000, Gold: 1000000
