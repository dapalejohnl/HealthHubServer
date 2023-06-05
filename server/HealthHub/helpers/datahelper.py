from helpers.healthscorehelper import exercise_types

class DefaultDataHelper():
	def getExerciseData():
		new_data = {}
		for exercise_name in exercise_types:
			new_data[exercise_name] = True
		return new_data