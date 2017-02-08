import string
import random

EXPECTED_STRING = "Hello world"

POPULATION_SIZE = 100

GENERATION_COUNT_MAX = 10000

CHANCE_TO_MUTATE = 0.1
GRADED_RETAIN_PERCENT = 0.2
CHANCE_RETAIN_NONGRATED = 0.05

GRADED_INDIVIDUAL_RETAIN_COUNT = (POPULATION_SIZE * GRADED_RETAIN_PERCENT)

MAX_SCORE = len(EXPECTED_STRING)

def get_random_char():
    return random.choice(string.ascii_letters + ' ')

def generate_individual():
	individual = ""
	for _ in range(len(EXPECTED_STRING)):
		individual += get_random_char()
	return individual

def generate_population():
	return [generate_individual() for _ in range(POPULATION_SIZE)]

def get_individual_score(individual):
	score = 0
	for c, expected_c in zip(individual, EXPECTED_STRING):
		if(c == expected_c):
			score += 1
	return score

def order_population_by_score(population):
	order_population = []
	for individual in population:
		order_population.append((individual, get_individual_score(individual)))
	return sorted(order_population, key=lambda x: x[1], reverse=True)

def evol_population(population):
	ordered_population = order_population_by_score(population)
	solution = []

	for individual, score in ordered_population:
		if(score == MAX_SCORE):
			solution.append(individual)

	if solution:
		return population, solution

	parents = ordered_population[:GRADED_INDIVIDUAL_RETAIN_COUNT]

	# Promote random individual for diversity
	for individual in order_population[GRADED_INDIVIDUAL_RETAIN_COUNT:]:
		if(random() < CHANCE_RETAIN_NONGRATED):
			parents.append(individual)

	# Random mutation
	for individual as parents:
		if random() < CHANCE_TO_MUTATE:
			place_to_modify = random.randint(0, MAX_SCORE)
            individual[place_to_modify] = get_random_char()

    # Crossover parent to create child
    

def main():
	print(order_population_by_score(generate_population()))

main()