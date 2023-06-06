from users.models import UserSettings, PlanEvent, HealthEvent
import math
from random import choice

exercise_types = [
	"yoga",
	"pilates",
	"cycling",
	"stretching",
	"tai chi",
	"weightlifting",
	"rowing",
	"squats",
	"walking",
	"running",
	"hiking",
	"elliptical",
	"pushups",
	"swimming",
	"dance",
	"lunges",
	"boxing",
]
exercise_met_vals = {
	"yoga": 1.5,
	"pilates": 2,
	"cycling": 4,
	"stretching": 1.3,
	"tai chi": 2.5,
	"weightlifting": 5,
	"rowing": 5,
	"squats": 2.5,
	"walking": 2,
	"running": 4,
	"hiking": 2.5,
	"elliptical": 3,
	"pushups": 3,
	"swimming": 5,
	"dance": 3,
	"lunges": 3,
	"boxing": 4,
}

meal_types = ["protein & vegtables", "protein pasta", "protein salad", "soup & salad", "banana", "smoothie", "salad"]
meal_vals = {
	"protein & vegtables": [700, 1500],
	"protein pasta": [700, 1200],
	"protein salad": [300, 500],
	"soup & salad": [300, 600],
	"banana": [80, 120],
	"smoothie": [100, 600],
	"salad": [0, 100],
}

def clamp(n, min_n, max_n):
	return max(min(n, max_n), min_n)

class HealthScores():
	def getIdealScore(user_uid, plan_type):
		# Use previous executed plans as a priority
		days_considered = 7
		goal_multiplier = 1.15
		avg_exercise_score = 0
		avg_meal_score = 0
		avg_sleep_score = 0
		
		exercise_events = PlanEvent.objects.filter(userUID=user_uid, type="exercise").order_by("-createdTime")[:days_considered]
		meal_events = PlanEvent.objects.filter(userUID=user_uid, type="meal").order_by("-createdTime")[:days_considered]
		sleep_events = PlanEvent.objects.filter(userUID=user_uid, type="sleep").order_by("-createdTime")[:days_considered]
		
		# Exercise score
		if len(exercise_events) > 0:
			event_sum = 0
			for event in exercise_events:
				event_sum += event.score
			avg_exercise_score = event_sum / len(exercise_events)
		
		# Meal score
		if len(meal_events) > 0:
			event_sum = 0
			for event in meal_events:
				event_sum += event.score
			avg_meal_score = event_sum / len(meal_events)
		
		# Sleep score
		if len(sleep_events) > 0:
			event_sum = 0
			for event in sleep_events:
				event_sum += event.score
			avg_sleep_score = event_sum / len(sleep_events)
				
		if plan_type == "exercise":
			if avg_exercise_score <= 50:
				# Use previous energy burned data to get a better understanding of a newer user
				# Only pull data that may show actual calories being burned
				energy_burned_events = HealthEvent.objects.filter(
					userUID=user_uid, 
					type="HKQuantityTypeIdentifierActiveEnergyBurned",
					value__gte=5
				).order_by("-createdTime")[:1000]
				
				if len(energy_burned_events) > 0:
					new_avg_score = 0
					for event in energy_burned_events:
						new_avg_score += event.value
					avg_exercise_score = new_avg_score / len(energy_burned_events)
				
			return int(clamp(avg_exercise_score, 100, 2500) * goal_multiplier)
		elif plan_type == "meal":
			# do more stuff in here for context
			
			
			
			return int(clamp(avg_meal_score, 100, 2500) * goal_multiplier)
		elif plan_type == "sleep":
			# do more stuff in here for context
			
			
			return int(clamp(avg_sleep_score, 14400, 50400) * goal_multiplier)
		return 0

	def getRecommendationByScore(user_uid, plan_type, score):
		user_settings = UserSettings.objects.get(userUID=user_uid)
		user_weight = user_settings.weight
		allowed_exercises = user_settings.exercises
		
		if plan_type == "exercise":
			# Pick a random allowed exercise
			allowed = []
			for exercise_name in allowed_exercises:
				allowed.append(exercise_name)
			rand_choice = choice(allowed)
			if rand_choice:
				met_val = exercise_met_vals[rand_choice]
				exercise_duration = int(score * 200 / (met_val * 3.5 * user_weight)) * 60
				return {"type": "exercise", "name": rand_choice, "duration": exercise_duration}
		elif plan_type == "meal":
			# Pick a random meal type that has an acceptable range
			allowed = []
			for meal_name in meal_types:
				range_list = meal_vals[meal_name]
				if score >= range_list[0] and score <= range_list[1]:
					allowed.append(meal_name)
			rand_choice = choice(allowed)
			if rand_choice:
				rounded_score = int(score - (score % 10))
				return {"type": "meal", "name": rand_choice, "calories": rounded_score}
		elif plan_type == "sleep":
			rounded_score = int(score - (score % 100))
			return {"type": "sleep", "duration": rounded_score}

	def getPlanPointValue(user_uid, plan):
		user_settings = UserSettings.objects.get(userUID=user_uid)
		user_weight = user_settings.weight
		
		if plan.get("type") == "exercise":
			mins_duration = math.ceil(plan.get("duration") / 60)
			met_val = exercise_met_vals[plan.get("name")]
			
			#Bushman B PhD. Complete Guide to Fitness and Health 2nd Edition. American College of Sports Medicine. Human Kinetics. 2017.
			score = mins_duration * (met_val * 3.5 * user_weight) / 200
			
			return score
		elif plan.get("type") == "meal":
			return plan.get("calories")
		elif plan.get("type") == "sleep":
			return plan.get("duration")
		return 0

	def getPlanScoreRatio(user_uid, ideal_plan, chosen_plan):
		ideal_score = HealthScores.getPlanPointValue(user_uid, ideal_plan)
		chosen_score = HealthScores.getPlanPointValue(user_uid, chosen_plan)
		if ideal_score != 0 and chosen_score != 0:
			return chosen_score / ideal_score
		return 0