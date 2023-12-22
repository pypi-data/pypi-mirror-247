import random

# Number of queens
N = 4

# Function to initialize population
def initialize_population(population_size):
    return [random.sample(range(N), N) for _ in range(population_size)]

# Fitness function
def fitness(chromosome):
    horizontal_collisions = sum([chromosome.count(queen)-1 for queen in chromosome])/2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
    
    return int(maxFitness - (horizontal_collisions + diagonal_collisions))

# Function to perform crossover
def crossover(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

# Function to perform mutation
def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

# Function to select population for next generation
def genetic_queen(population, fitness):
    mutation_probability = 0.03
    new_population = []
    probabilities = [fitness(n) for n in population]
    # Elitism: Preserve the best 10% of the population
    elite_size = int(0.1 * len(population))
    elites = sorted(population, key=fitness, reverse=True)[:elite_size]
    for i in range(len(population) - elite_size):
        x = random.choices(population, weights=probabilities)[0]
        y = random.choices(population, weights=probabilities)[0]
        child = crossover(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    # Add the elites to the new population
    new_population.extend(elites)
    return new_population
# Function to check if any individual has reached the goal
def check_population(population, fitness):
    current_max_fitness = max([fitness(n) for n in population])
    print("Max Fitness = {}".format(current_max_fitness))
    best_chromosome = population[[fitness(n) for n in population].index(current_max_fitness)]
    print("Best Chromosome = {}".format(best_chromosome))
    if current_max_fitness == maxFitness: return True
    return False

# Driver code
if __name__ == "__main__":
    maxFitness = (N*(N-1))/2  # 6
    population = initialize_population(2)

    generation = 1

    while not check_population(population, fitness):
        print("Generation = {}".format(generation))
        population = genetic_queen(population, fitness)
        print("\n")
        generation += 1