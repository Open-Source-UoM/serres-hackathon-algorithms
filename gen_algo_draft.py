from datetime import time
from functools import partial
from random import random
from typing import List, Callable, Tuple

Genome = List[int]
Population = List[Genome]
FitnessFunc = Callable[[Genome], int]
PopulateFunc = Callable[[], Population]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossOverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]


def generate_genome(length: int) -> Genome:
    return random.choices([0, 1], k=length)

def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]

def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")
    length = len(a)
    if length < 2:
        return a, b
    p = random.randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]

def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):
        index = random.randint(0, len(genome) - 1)
        genome[index] = genome[index] if random.random() > probability else abs(genome[index] - 1)
    return genome

def population_fitness(population: Population, fitness_func: FitnessFunc) -> int:
    return sum([fitness_func(genome) for genome in population])

def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return random.choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2
    )

def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)

def genome_to_string(genome: Genome) -> str:
    return "".join(map(str, genome))

def run_evolution(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    fitness_limit: int,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossOverFunc = single_point_crossover,
    mutation_func: MutationFunc = mutation,
    generation_limit: int = 100
) -> Tuple[Population, int]:
    population = populate_func()

    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness_func(genome),
            reverse=True
        )

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]

        population = next_generation

    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )

    return population, i

start_time = time.time()
populations, generations = run_evolution(
    populate_func=partial(
        generate_population,
        size=10,
        genome_length=10 # edw 8a xreiastein a mpei to size apo to thing poy 8a exoume
    ),
    fitness_func=partial(
        population_fitness,
        target="Hello, World!" # edw prepei na mpei weight kai thing
    ),
    fitness_limit=13,
    generation_limit=100
)
end_time = time.time()

print(f"number of generations: {generations}")
print(f"time: {end_time - start_time}s")
print(f"result: {genome_to_string(populations[0])}")





