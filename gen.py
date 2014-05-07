#!/usr/bin/python
#this is the genetic algorithm described in french linux magazine edition of may 2014.
#the goal is to find the closest numerical expression closest to a given number (1234 here)
# each expression is a set of 12 genes
# A gene can code the following value : 0,1,2,3,4,5,6,7,8,9,+,-,/,%,(and _ two times for empy value)
# a numerical expression is a sentence composed of 12 genes 
# All genes are binary encoded (0000=0, 0001=1,...)
# There is a expression selection which select the best expression
# there is a reproduction function to make a new population based on the selected best previous expression
# there is a mutation function to introduce randomness into reproduction
# currently the value are set to 100000 generations (before stopping).
# a set of 1000 expressions as population 
# a value of 50% mutation. 

import random
import sys

def chromosome_initial(nb_genes=12, taille_gene=4):
    chromosome =""
    for i in range(nb_genes):
        for j in range(taille_gene):
            chromosome += str(random.randint(0,1))
    return chromosome

def population_initiale(individus=1000):
    population = []
    for i in range(individus):
        population.append((None,chromosome_initial()))
    return population


def gene_to_symbole(gene,codage):
    return codage[int(gene,2)]

def chromosome_to_expression(chromosome,codage,taille_gene=4):
    expression =""
    for num_gene in range(int(len(chromosome)/taille_gene-1)):
        expression += gene_to_symbole(chromosome[num_gene *4:num_gene*4+4],codage)
        #print(expression)
    return expression

def fitness(chromosome, codage, taille_gene=4,resultat_final=1234):
    expression = chromosome_to_expression(chromosome,codage,taille_gene)
    try:
        resultat= abs(resultat_final- eval(expression))
    except:
        resultat = sys.maxsize
    #print(resultat)
    return resultat

def evaluer_population(population, codage, taille_gene=4, resultat_final=1234):
    for indice, (value, chromosome) in enumerate(population):
        population[indice]=(fitness(chromosome, codage, taille_gene, resultat_final), chromosome)
    population.sort()

def selection(population, pourcentage=0.5):
    return population[0:int(len(population)*pourcentage)]

def crossingover(parent1, parent2):
    chromosome1= parent1[1]
    chromosome2= parent2[1]
    point_croisement = random.randint(1,len(chromosome1)-2)
    enfant1 = (None, chromosome1[0:point_croisement]+chromosome2[point_croisement:])
    enfant2 = (None, chromosome2[0:point_croisement]+chromosome1[point_croisement:])
    return [enfant1,enfant2]

def mutation(individu):
    chromosome= individu[1]
    base = random.randint(0,len(chromosome) -1)
    mute = "1" if chromosome[base] == "0" else "1"
    chromosome = chromosome[0:base]+mute+chromosome[base+1:]
    return [None, chromosome]

def nouvelle_generation(population,codage,taille_gene=4, resultat_final=1234, taux_selection=0.5, taux_crossingover=0.9, taux_mutation=0.5):
    evaluer_population(population,codage,taille_gene,resultat_final)
    population= selection(population, taux_selection)
    meilleur = population[0][0]
    meilleur_eval = chromosome_to_expression(population[0][1], codage)
    random.shuffle(population)
    nouvelle_population= []
    indice = 0
    taille_population = len(population)
    while (indice + 1) < taille_population:
        parent1= population[indice]
        parent2= population[indice+1]
        indice +=2
        if random.random() <= taux_crossingover:
            for i in range(int(1/taux_selection)):
                nouvelle_population += crossingover(parent1,parent2)
        else:
            for i in range(int(1/taux_selection)):
                nouvelle_population.append(parent1)
                nouvelle_population.append(parent2)
    for individu in nouvelle_population:
        if random.random() <= taux_mutation:
            nouvelle_population[indice] = mutation(individu)
    return (meilleur, meilleur_eval, nouvelle_population)


if __name__ == "__main__":
    codage=("0","1","2","3","4","5","6","7","8","9","+","-","/","%","_","_")
    n_generation = 0
    P0= population_initiale()
    # for chromosome in P0:
    #     print(chromosome)
    #     print(chromosome_to_expression(chromosome,codage))
    #  evaluer_population(P0,codage)
    # P0=selection(P0)
    # print(P0)
    while True:
        meilleur_score, meilleur_evaluation, P1 = nouvelle_generation(P0,codage)
        P0=P1
        n_generation +=1
        print("Generation: {} Meilleur score: {}".format(n_generation, meilleur_score))
        print("     {}".format(meilleur_evaluation))
        if meilleur_score == 0:
            break
        if n_generation == 100000:
            print("Il vaut mieux repartir sur une nouvelle population...")
            evaluer_population(P1,codage)
            print(P1)
            P0= population_initiale()
            n_generation = 0
#            print("Appuyez sur <Return> pour continuer")
#            input()
