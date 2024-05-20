import random

# Initialize a population with random permutations.
def initialize_population(pop_size, n):
    population = []
    for _ in range(pop_size):
        individual = random.sample(range(n), n)
        population.append(individual)
    return population


# Calculate the fitness of an individual.
def fitness(individual):
    non_conflicting_pairs = 0
    n = len(individual)
    for i in range(n):
        for j in range(i + 1, n):
            if not conflict(i, individual[i], j, individual[j]):
                non_conflicting_pairs += 1
    return non_conflicting_pairs


# Check if two queens conflict with each other.
def conflict(r1, c1, r2, c2):
    return c1 == c2 or abs(r1 - r2) == abs(c1 - c2)


# Select individuals from the population based on their fitness
def select(population, fitnesses):
    selected = []
    total_fitness = sum(fitnesses)
    for _ in range(len(population)):
        r = random.uniform(0, total_fitness)
        s = 0
        for i, individual in enumerate(population):
            s += fitnesses[i]
            if s >= r:
                selected.append(individual)
                break
    return selected


# Perform crossover between two parents to produce an offspring.
def crossover(parent1, parent2):
    n = len(parent1)
    c1, c2 = random.randint(0, n-1), random.randint(0, n-1)
    start, end = min(c1, c2), max(c1, c2)
    child = [-1] * n
    child[start:end+1] = parent1[start:end+1]
    pointer = 0
    for val in parent2:
        if val not in child:
            while child[pointer] != -1:
                pointer += 1
            child[pointer] = val
    return child


# Mutate an individual by swapping two random positions.
def mutate(individual):
    n = len(individual)
    idx1, idx2 = random.sample(range(n), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]


# Solve the N-Queens Problem using a genetic algorithm.
def genetic_algorithm(n, pop_size, max_generations, mutation_rate):
    population = initialize_population(pop_size, n)
    for generation in range(max_generations):
        fitnesses = [fitness(individual) for individual in population]
        if max(fitnesses) == n * (n - 1) // 2:
            break
        population = select(population, fitnesses)
        next_population = []
        for _ in range(pop_size // 2):
            parent1, parent2 = random.sample(population, 2)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            if random.random() < mutation_rate:
                mutate(child1)
            if random.random() < mutation_rate:
                mutate(child2)
            next_population.extend([child1, child2])
        population = next_population
    best_individual = max(population, key=fitness)
    return best_individual


# Print the N-Queens board with queens placed as per the solution.
def print_solution(solution):
    n = len(solution)
    board = [['.' for _ in range(n)] for _ in range(n)]
    for r, c in enumerate(solution):
        board[r][c] = 'Q'
    for row in board:
        print(' '.join(row))


# Parameters
n = int(input("Enter the size of the N-Queens board (n): "))
pop_size = int(input("Enter the population size: "))
max_generations = int(input("Enter the maximum number of generations: "))
mutation_rate = float(input("Enter the mutation rate (e.g., 0.1): "))

solution = genetic_algorithm(n, pop_size, max_generations, mutation_rate)
print("Solution:")
print_solution(solution)
