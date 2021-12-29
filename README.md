# INF05010-OTI-COMB

Trabalho final para a cadeira Otimização Combinatória do 5.º período da Universidade Federal Do Rio Grande Do Sul cursada no semestre 2020/2.

O trabalho se trata de resolver o problema do emparelhamento diversificado através do algoritmo genético.

# Arguments for the program:

-o, --outputFile, help=Name of the file to store the found solution, type=str.

-i, --Instance, type=str, help=Name of the Instance.Its important to be a txt file and not be between " ".

-t, --TimeLimit, type=int, default=1800,help=The maximum time that the program will execute.Positive integer.

-p, --Population, type=int, default=40,help="Size of the population. Should be a positive integer.

-m, --m_r, type=float, default=0.9,help="Represents the probability for the mutation to happen.Float between 0 and 1.

-g, --m_n_g, type=int, default=30,help="The maximum number of generations without improvement.Positive integer.

-n, --n_p_s, type=int, default=10,help="The number of new individuals that will be generated each generation .

-s, --seed, type=int, default=None,help="Seed for the random module.Random seed will be chosen if this parameter is not filled.

-v, -verbose, type=int, default=1,help=More detailed solution.Must be 1 for true and 0 for false.

# Example of Usage

python execute.py -o out -i data/RM01.txt -t 1800 -p 40 -m 0.9 -g 30 -n 10 -s 333 -v 1
