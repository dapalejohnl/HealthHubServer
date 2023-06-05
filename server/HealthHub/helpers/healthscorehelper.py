from users.models import UserSettings
import math

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

class HealthScores():
	def getPlanPointValue(user_uid, plan):
		user_settings = UserSettings.objects.get(userUID=user_uid)
		user_weight = user_settings.weight
		
		if plan.get("type") == "exercise":
			mins_duration = math.floor(plan.get("duration") / 60)
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