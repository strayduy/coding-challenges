#!/usr/bin/env python2.7

# Standard libs
import itertools
import sys

def main(input_handle):
    foods = []
    exercises = []
    zeroes = []

    # Read in each activity
    try:
        num_items = int(input_handle.readline())
        for i in range(num_items):
            activity, calories = input_handle.readline().strip().split()
            calories = int(calories)

            # Split the activities into three categories:
            # 1. Foods: Activities with a positive caloric impact
            # 2. Exercises: Activities with a negative caloric impact
            # 3. Zeroes: Activities with no caloric impact
            if calories > 0:
                foods.append(Activity(activity, calories))
            elif calories < 0:
                exercises.append(Activity(activity, calories))
            else:
                zeroes.append(Activity(activity, calories))
    except:
        raise Exception("Bad input")

    # Easy case! We have at least one activity that has an individual caloric
    # impact of zero. Return the first such activity.
    if zeroes:
        print zeroes[0].name
        return

    # Normal case: Find the combination of activities that result in a net
    # caloric impact of zero.
    zero_calorie_diet = find_zero_calorie_diet(foods, exercises)

    if zero_calorie_diet:
        # Print out the solution with the list of activities in alphabetical
        # order
        print "\n".join(sorted(zero_calorie_diet))
    else:
        print "no solution"

# Tries to find a set of foods and a set of exercises with an equal (but
# opposite) number of calories. Returns the result as a list of activity names
# (as strings).
# Returns None if there isn't any combination of foods and exercises that have
# an equivalent caloric impact.
def find_zero_calorie_diet(foods, exercises):
    # Sanity check
    if not foods or not exercises:
        return None

    # Algorithm:
    # Iterate over each possible combination of food items and each combination
    # of exercises, recording the caloric impact of each combination into a
    # map.
    # After each iteration, check whether the map contains an entry for the
    # opposite calorie value.
    # If such an entry exists, then we've found a pair of food and exercise
    # that cancel each other out.
    # We give up once we exhaust all possible combinations without finding a
    # match.

    # Maps a calorie value to a list of activities that result in that value
    calorie_map = {}

    # Iterate over an increasing number of activities to combine together for
    # each category
    for i in range(1, max(len(foods), len(exercises)) + 1):
        # Alternate between combining foods and exercises
        for category in [foods, exercises]:
            # Iterate over the combinations of activities of size 'i'
            for combo in itertools.combinations(category, i):
                # Compute the combined number of calories for this combination
                # of activities
                combined_calories = sum([activity.calories for activity in combo])

                # If we haven't seen this combined calorie value before, then
                # record the names of the activities that resulted in this
                # calorie value
                if combined_calories not in calorie_map:
                    activity_names = [activity.name for activity in combo]
                    calorie_map[combined_calories] = activity_names

                    # Then, check whether we've recorded a list of activities
                    # that have resulted in the opposite number of calories.
                    if combined_calories * -1 in calorie_map:
                        # If such a list of activities exists, then we've
                        # found our Dropbox diet.
                        # Return the combined list of activity names.
                        diet = activity_names + calorie_map[combined_calories * -1]
                        return diet

    # If we've reached this point, then we didn't find a set of activities that
    # resulted in zero net calories.
    return None

class Activity:
   def __init__(self, name=None, calories=0):
       self.name = name
       self.calories = calories

   def __str__(self):
       return "<%s, %d>" % (self.name, self.calories)

   def __repr__(self):
       return str(self)

if __name__ == "__main__":
    main(sys.stdin)
