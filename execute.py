import argparse
from rm_ag import run_ga_oficial
from rm_ag import read_instance


def parseInput():
    """
    Parse the input from the command line
    :return: Return a tuple with the parameters parsed.
    """
    parser = argparse.ArgumentParser(description='INF05010 - Final Project')

    parser.add_argument('-o', '--outputFile', help='Name of the file to store the found solution', type=str)
    parser.add_argument("-i", "--Instance", type=str, help="Name of the Instance.Its important to be a txt file and "
                                                           "not be between " " ")
    parser.add_argument("-t", "--TimeLimit", type=int, default=1800,
                        help="The maximum time that the program will execute.Positive integer.")
    parser.add_argument("-p", "--Population", type=int, default=40,
                        help="Size of the population. Should be a positive integer")
    parser.add_argument("-m", "--m_r", type=float, default=0.9,
                        help="Represents the probability for the mutation to happen.Float between 0 and 1.")
    parser.add_argument("-g", "--m_n_g", type=int, default=30,
                        help="The maximum number of generations without improvement.Positive integer.")
    parser.add_argument("-n", "--n_p_s", type=int, default=10,
                        help="The number of new individuals that will be generated each generation .")
    parser.add_argument("-s", "--seed", type=int, default=None,
                        help="Seed for the random module.Random seed will be chosen if this parameter is not filled.")
    parser.add_argument("-v", "--verbose", type=int, default=1,
                        help="More detailed solution.Must be 1 for true and 0 for false")

    args, unknown = parser.parse_known_args()

    invalid_params(args.outputFile,args.Instance,args.TimeLimit, args.Population, args.m_r, args.m_n_g, args.n_p_s, args.verbose)

    return args.outputFile, args.Instance, args.TimeLimit, args.Population, args.m_r, args.m_n_g, args.n_p_s, args.seed, args.verbose


def invalid_params(out,instance,time, pop, mr, m_n_g, n_p_s, verbose):
    """

    :param time: max_time given
    :param pop: size of the population given
    :param mr: mutation rate given
    :param m_n_g: max_non_improving_generation given
    :param n_p_s: size of new generated individuals given
    :param verbose: verbose given
    :return:
    """
    if out is None:
        print("An output file must be informed.")
        exit(1)
    if instance is None:
        print("An Instance file must be informed.")
        exit(1)
    if time <= 0:
        print("The time limit  must be a positive integer.")
        exit(1)
    if pop <= 0:
        print("The  Population_Size must be a positive integer.")
        exit(1)
    if mr < 0 or mr > 1:
        print("Mutation_Rate must be a float between 0 and 1.")
        exit(1)
    if m_n_g <= 0:
        print("Max_Non_Improving_Gen must be a positive integer.")
        exit(1)
    if n_p_s <= 0:
        print("New_p_Size must be a positive integer.")
        exit(1)
    if verbose < 0 or verbose > 1:
        print("Verbose must be 0 for false and 1 for true")
        exit(1)


def save_solution(output, instance, best, evaluate, time, v):
    """
    This function writes in the output file the best solution found.
    :param output: Name of the file to store the found solution
    :param instance: Name of the Instance
    :param best:  Chromosome representing the best solution
    :param evaluate:  Fitness of the best chromosome
    :param time: Execution time
    :param v: Verbose
    :return: None
    """
    with open(output + ".txt", 'w') as out:
        out.write("Instance name:\n" + instance + '\n\n')
        out.write("Time: \n" + str(time) + '\n\n')
        out.write("Objective Value:\n" + str(evaluate) + '\n\n')
        out.write("Solution: \n" + str(best) + '\n\n')
        if v:
            out.write('Detailed Solution(Edges that make part of the matching):\n')
            vertices_1 = []
            vertices_2 = []
            colors = []
            v1, v2, color = read_instance(instance)
            for i in range(len(best)):
                if best[i] == 1:
                    vertices_1.append(v1[i])
                    vertices_2.append(v2[i])
                    colors.append(color[i])
            out.write('# vertice1 vertice2 cor \n')
            for i in range(len(vertices_1)):
                out.write(str(vertices_1[i]) + ' ' + str(vertices_2[i]) + ' ' + str(
                    colors[i]) + ' ' + '\n')


def print_solution(instance, best, evaluate, time, v):
    """
    This function print the best solution found.

    :param instance: Name of the Instance
    :param best:  Chromosome representing the best solution
    :param evaluate:  Fitness of the best chromosome
    :param time: Execution time
    :param v: Verbose
    :return: None
    """
    print("Instance name:\n" + instance + '\n\n')
    print("Time: \n" + str(time) + '\n\n')
    print("Objective Value:\n" + str(evaluate) + '\n\n')
    print("Solution: \n" + str(best) + '\n\n')
    if v:
        print('Detailed Solution(Edges that make part of the matching):\n')
        vertices_1 = []
        vertices_2 = []
        colors = []
        v1, v2, color = read_instance(instance)
        for i in range(len(best)):
            if best[i] == 1:
                vertices_1.append(v1[i])
                vertices_2.append(v2[i])
                colors.append(color[i])
        print('# vertice1 vertice2 cor \n')
        for i in range(len(vertices_1)):
            print(str(vertices_1[i]) + ' ' + str(vertices_2[i]) + ' ' + str(
                colors[i]) + ' ' + '\n')


def main():
    outFile, instance, t, m, p, s, n, seed, verbose = parseInput()
    print(instance)
    best, eval_best, time = run_ga_oficial(instance, n, m, p, s, t, seed=seed)
    save_solution(outFile, instance, best, eval_best, time, verbose)
    print_solution(instance, best, eval_best, time, verbose)


if __name__ == "__main__":
    main()
