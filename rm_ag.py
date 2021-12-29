import random
# import sys
import time
import copy

# from operator import itemgetter
# import matplotlib.pyplot as plt
import numpy as np


def read_instance(filea):
    """
    Read the instance file
    :param filea: Instance file
    :return: Return a tuple with 3 elements(list of vertices 1, list of vertices 2,and list of colors)
    """

    with open(filea, "r") as myfile:
        next(myfile)
        next(myfile)
        next(myfile)
        next(myfile)
        data = myfile.readlines()

    lst_aux = [j.rstrip() for j in data]
    lst_split = [i.split() for i in lst_aux]
    v1 = []
    v2 = []
    color = []
    for i in lst_split:
        v1.append(int(i[0]))
        v2.append(int(i[1]))
        color.append(int(i[2]))
    return v1, v2, color


def gen_random_pop_2(file):
    """
    This function generate a random population, and refactibilize the solution based on the chosen edge
    :param file: Instance file
    :return: Return a tuple with 4 elements(individuo,vertices1,vertices2,cores)
    """
    v1, v2, color = read_instance(file)
    v1_in = []
    v2_in = []
    c_in = []
    lst_alleles = [random.randint(0, 1) for _ in range(len(v1))]
    # print(len(lst_alleles))
    ind = random.randint(0, len(v1) - 1)
    while lst_alleles[ind] == 0:
        ind = random.randint(0, len(v1) - 1)
    v1_in.append(v1[ind])
    v2_in.append(v2[ind])
    c_in.append(color[ind])
    # print(lst_alleles,ind)

    for i in range(len(lst_alleles)):

        if (lst_alleles[i] == 1) and ((v1[i] in v1_in) or (v1[i] in v2_in) or (v2[i] in v1_in) or (
                v2[i] in v2_in) or (color[i] in c_in)) and i != ind:
            lst_alleles[i] = 0
        else:
            if lst_alleles[i] == 1:
                v1_in.append(v1[i])
                v2_in.append(v2[i])
                c_in.append(color[i])
    # print(v1_in)
    # print(v2_in)
    # print(eval(lst_alleles),lst_alleles)
    return lst_alleles, v1_in, v2_in, c_in


'''
def check(l1, l2, l3):
    l1_check = True
    l2_check = True
    l3_check = True
    for i in range(len(l1)):
        if l1[i] in l2:
            l1_check = False
    for i in range(len(l2)):
        if l2[i] in l1:
            l2_check = False
    set_l1 = set(l1)
    set_l2 = set(l2)
    if len(set_l1) != len(l1):
        l1_check = False
    if len(set_l2) != len(l2):
        l2_check = False
    if len(l3) != len(set(l3)):
        l3_check = False
    print(l1_check, l2_check, l3_check)
'''


def evaluate(individual):
    """
    This function evaluate the fitness of the individual
    :param individual: individual tha will be evaluate
    :return: Fitness of the individual
    """
    return np.sum(individual)


def tournament(participants):
    """
    This function implements the tournament method
    :param participants:List of the individuals
    :return:Best individual found
    """
    lst_conflitos = [evaluate(x) for x in participants]
    # print(lst_conflitos)
    index = lst_conflitos.index(max(lst_conflitos))
    # print(participants[index])
    return participants[index]


def uni_crossover(parent1, parent2):
    """
    This function implements the uniform crossover method,where each gene of the parent1 has 50% of chance to swap
    with the correspondent gene of parent2
    :param parent1:List represent the parent1
    :param parent2:List represent the parent2
    :return:Return a tuple with 2 elements representing the new individuals generated
    """
    size = min(len(parent1), len(parent2))
    for i in range(size):
        if random.randint(0, 1) < 0.5:
            parent1[i], parent2[i] = parent2[i], parent1[i]

    return parent1, parent2


def refactibilize(individual, file):
    """
    This function turn the individual feasible
    :param individual: individual that will be turned feasible
    :param file: Instance file
    :return:Return the feasible individual
    """
    v1, v2, color = read_instance(file)
    v1_in = []
    v2_in = []
    c_in = []

    for i in range(len(individual)):

        if (individual[i] == 1) and ((v1[i] in set(v1_in)) or (v1[i] in set(v2_in)) or (v2[i] in set(v1_in)) or (
                v2[i] in set(v2_in)) or (color[i] in set(c_in))):
            individual[i] = 0
        else:
            if individual[i] == 1:
                v1_in.append(v1[i])
                v2_in.append(v2[i])
                c_in.append(color[i])

    # print(individual)
    return individual


def mutate(individual, m, k):
    """
    This function apply the mutation operator
    :param k:Number of genes that were chosen to maybe mutate
    :param individual:list
    :param m:Mutation Rate
    :return:Return the individual after the mutation
    """

    lst = random.sample(range(0, len(individual)), k)
    # print(lst)
    for i in lst:
        if random.random() < m:
            if individual[i] == 0:
                individual[i] = 1
    # print(individual)
    return individual


def remove_ind(lst, num):
    """
    This function remove the num worsts individuals from the lst
    :param lst: list of individuals that will be evaluated
    :param num: Number of individuals that will be removed from the list(population)
    :return: Return the list(population) with num individuals removed
    """
    aux = [evaluate(x) for x in lst]
    # print(aux)
    for i in range(num):
        index = aux.index(min(aux))
        # print(index)
        del lst[index]
        del aux[index]

    return lst


def run_ga_oficial(file, new_i=10, population_size=40, mutation_rate=0.9, max_non_gen=30, max_time=1800, k=25,seed=None):
    """
    This function apply the metaheuristic genetic algorithm
    :param file: Instance File
    :param new_i: Number of new individuals generated each generation
    :param population_size: Size of the population
    :param mutation_rate: Probability for the mutation to happen
    :param max_non_gen: Max non improving generations
    :param max_time: Max time for the program to execute
    :param k: number of individuals that will participate in the tourney
    :param seed: seed used to generate the solution
    :return: Return a tuple with 3 elements(best individual, fitness of the best individual,time passed)
    """
    random.seed(seed)
    # generate  inicial population
    p = []
    start_time = time.time()
    for j in range(population_size):
        # print(i)
        a, b, c, d = gen_random_pop_2(file)
        p.append(a)

    # start best solution with the best of the population
    best_ini = tournament(p)
    best = copy.deepcopy(best_ini)
    # start non improving generation with 0
    non_gen = 0
    # print(evaluate(best))
    while (non_gen < max_non_gen) and time.time() - start_time <= max_time:
        # start new population empty
        p_ = []
        while len(p_) < new_i and time.time() - start_time <= max_time:
            # tournament
            p1 = tournament(random.sample(p, k))
            p2 = tournament(random.sample(p, k))
            # crossover
            o1, o2 = uni_crossover(p1, p2)
            # mutation
            o1 = mutate(o1, mutation_rate, random.randint(0, int(len(p1) / 3)))
            o2 = mutate(o2, mutation_rate, random.randint(0, int(len(p1) / 3)))
            # append new population
            p_.append(o1)
            p_.append(o2)
        # turn individuals of the new_population feasible
        for e in p_:
            e = refactibilize(e, file)
            # append new population in population
            p.append(e)
        # remove new_i worsts individuals of the population
        p = copy.deepcopy(remove_ind(p, new_i))

        # print(evaluate(best))

        # best solution of the new current generation
        new_best = tournament(p)

        # if the new solution is better then the previous best one ,
        # the best solution turns the new solution and non improving generations is set to 0
        # else non improving generations + 1
        if evaluate(new_best) <= evaluate(best):
            non_gen += 1
        else:
            best = copy.deepcopy(new_best)
            non_gen = 0
        # print(evaluate(best), non_gen)

    # print(time.time() - start_time)
    # print(evaluate(best))

    # return the best individual, the fitness of the best individual, time elapsed
    return best, evaluate(best), time.time() - start_time
