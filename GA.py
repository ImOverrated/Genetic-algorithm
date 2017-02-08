import string
import random
import math
import pygal

EXPECTED_STRING = "Hello world"

POPULATION_SIZE = 100

GENERATION_COUNT_MAX = 10000000

CHANCE_TO_MUTATE = 0.1
GRADED_RETAIN_PERCENT = 0.2
CHANCE_RETAIN_NONGRATED = 0.05

GRADED_INDIVIDUAL_RETAIN_COUNT = int(POPULATION_SIZE * GRADED_RETAIN_PERCENT)

MAX_SCORE = len(EXPECTED_STRING)
MIDDLE_LENGTH = len(EXPECTED_STRING) / 2
if not MIDDLE_LENGTH.is_integer:
	LEFT_LENGTH = int(round(MIDDLE_LENGTH))
	RIGHT_LENGTH = int(math.floor(MIDDLE_LENGTH))
else:
	LEFT_LENGTH = int(MIDDLE_LENGTH)
	RIGHT_LENGTH = int(MIDDLE_LENGTH)

def get_random_char():
    return random.choice(string.ascii_letters + ' ')

def generate_individual():
	individual = []
	for _ in range(len(EXPECTED_STRING)):
		individual.append(get_random_char())
	return individual

def generate_population():
	return [generate_individual() for _ in range(POPULATION_SIZE)]

def get_individual_score(individual):
	score = 0
	for c, expected_c in zip(individual, EXPECTED_STRING):
		if(c == expected_c):
			score += 1
	return score

def average_population_score(population):
	total = 0
	for individual in population:
		total += get_individual_score(individual)
	return total / POPULATION_SIZE

def order_population_by_score(population):
	order_population = []
	for individual in population:
		order_population.append((individual, get_individual_score(individual)))
	return sorted(order_population, key=lambda x: x[1], reverse=True)

def evol_population(population):
	raw_order_population = order_population_by_score(population)
	solution = []
	order_population = []

	for individual, score in raw_order_population:
		order_population.append(individual)
		if(score == MAX_SCORE):
			solution.append(individual)

	if solution:
		return population, average_population_score(population), solution

	parents = order_population[:GRADED_INDIVIDUAL_RETAIN_COUNT]

	# Promote random individual for diversity
	for individual in order_population[GRADED_INDIVIDUAL_RETAIN_COUNT:]:
		if(random.random() < CHANCE_RETAIN_NONGRATED):
			parents.append(individual)

	# Random mutation
	for individual in parents:
		if(random.random() < CHANCE_TO_MUTATE):
			place_to_modify = random.randint(0, MAX_SCORE - 1)
			individual[place_to_modify] = get_random_char()

    # Crossover parent to create child
	parents_len = len(parents)
	desired_len = POPULATION_SIZE - parents_len
	children = []
	while(len(children) != desired_len):
		#print(str(len(children)) + ' //// ' + str(desired_len))
		father = random.choice(parents)
		mother = random.choice(parents)

		child = father[:LEFT_LENGTH] + mother[RIGHT_LENGTH:]
		children.append(child)

	parents.extend(children)
	return parents, average_population_score(population), solution


def main():
	# Create population
	population = generate_population()
	average_score = average_population_score(population)
	print("Starting score  : " + str(average_score))

	# Evolve population
	i = 0
	solution = None
	log_avg = []
	while not solution and i < GENERATION_COUNT_MAX:
		population, average_score, solution = evol_population(population)
		if i & 255 == 255:
			print("Current score : " + str(average_score))
		if i & 31 == 31:
			log_avg.append(average_score)
		i+=1

	# Generation de l'évolution du score de la population
	line_chart = pygal.Line(show_dots=False, show_legend=False)
	line_chart.title = "Score evolution"
	line_chart.x_title = "Generations"
	line_chart.y_title = "Score"
	line_chart.add("Score", log_avg)
	line_chart.render_to_file("bar_chart.svg")

	final_average_score = average_population_score(population)
	print("Final Score : " + str(final_average_score))

	if solution:
		print("Solution found (%d times) after %d generations." % (len(solution), i))
	else:
		print("No solution found after %d generations." % i)
		print("- Last population was:")
		for number, individual in enumerate(population):
			print(number, '->',  ''.join(individual))

main()
			
