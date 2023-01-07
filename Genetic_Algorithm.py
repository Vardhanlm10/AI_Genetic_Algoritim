from Graph_Creator import *
import time
import numpy as np
import matplotlib.pyplot as plt
import csv

# def fitness_value(vertices,edges):
#     fitness = []
#     for i in range(len(edges)):
#         edge = edges[i]
#         x = edge[0]
#         y = edge[1]

#         if vertices[x]!=vertices[y]:
#             if [x,y] or [y,x] not in fitness:
#                 fitness.append([x,y])
#     return len(fitness)
def fitness_value(vertices,edges):
    fitness = 0
    neighbours = {}
    for i in range(50):
        neighbours[i] = []

    for i in range(len(edges)):
        edge = edges[i]
        neighbours[edge[0]].append(edge[1])
        neighbours[edge[1]].append(edge[0])
    
    for i in range(50):
        neighbour = neighbours[i]
        x = 1
        if len(neighbour)!=0:
            for nei in neighbour:
                if vertices[i]==vertices[nei]:
                    x = 0
        if x==1:
            fitness+=1
    return fitness
        

def takeSecond(elem):
    return elem[1]

def weighted_by(population):
    weights = []
    total = 0
    for i in range(len(population)):
        total+=population[i][1]
    
    for i in range(len(population)):
        weights.append(population[i][1]/total)

    return weights

# def reproduce(parent1,parent2):
#     n = 50
#     c = np.random.randint(10,40)
#     child = {}
#     for i in range(c):
#         child[i] = parent1[i]
#     i = c
#     while i < n:
#         child[i] = parent2[i]
#         i+=1
#     return child
def reproduce(parent1,parent2):
    n = 50
    child = {}
    for i in range(n):
        x = np.random.choice([0,1],1,p=[0.5,0.5])
        if x==0:
            child[i]= parent1[i]
        else:
            child[i] = parent2[i]
    return child 

        

def mutate(child):
    for i in range(50):
        to_mut = np.random.choice([0,1],1,p=[0.98,0.02])
        if to_mut==1:
            child[i] = np.random.choice(['R','G','B'])
    return child

def Genetic_Algorithm(population,edges):
    start = time.time()
    j = 0
    max_fit = population[0]
    fitness = []
    elite = 3
    cull = 3

    iterations = 50
    
    end = 0
    while (end-start) < 45:
        end = time.time()
        weights = weighted_by(population[0:len(population)-cull])
        population.sort(key=takeSecond)
        population2 = []
        for x in range(elite):
            population2.append(population[len(population)-1-x])
        for i in range(len(population)-elite):
            parent1 , parent2 = np.random.choice([population[i+cull][0] for i in range(len(population)-cull)],2,p=weights)
            child = reproduce(parent1,parent2)
            
            child = mutate(child)
            fitness_c = fitness_value(child,edges)
            if max_fit[1]<fitness_c:
                max_fit = [child , fitness_c]
            population2.append([child,fitness_c])
        population = population2
        if max_fit[1]>=50:
            break
        fitness.append(max_fit[1])
        j+=1
        
    return max_fit,fitness,end-start

            ##implement reproduce and mutation functions
            


    


def main():
    gc = Graph_Creator()

#    ********* You can use the following two functions in your program
    print("Roll no: 2020A7PS0982G")
    
    edges = gc.ReadGraphfromCSVfile("Testcases/200")
    
    # edges = gc.CreateGraphWithRandomEdges(50) # Creates a random graph with 50 vertices and 200 edges

    print("Number of Edges : {}".format(len(edges)))
    # edges = gc.ReadGraphfromCSVfile("test_case") # Reads the edges of the graph from a given CSV file
    # print(len(edges))
    # print()
    choices = []
    population = []
    for i in range(20):
        vertices = {}

        for i in range(50):
            x = np.random.randint(0,3)
            if x==0:
                vertices[i] = "R"
            elif x==1:
                vertices[i] = "G"
            else:
                vertices[i] = "B"
        
        
        fitness = fitness_value(vertices,edges)
        choices.append([vertices , fitness])
        

    choices.sort(key=takeSecond)
    
    
    for j in range(15):
        population.append(choices[20-1-j])
    

    weights = weighted_by(population)

    max_fit , fitness , execution_time = Genetic_Algorithm(population,edges)
    print("Best state :")
    print(max_fit[0])
    print("Fitness Value of best state : {}".format(max_fit[1]))
    print('Time taken : {}'.format(execution_time))

    x_val = range(len(fitness))
    plt.plot(x_val,fitness)
    plt.xlabel('Iterations')
    plt.ylabel('Best fit value')
    plt.show()

#    **********
#    Write your code for find the optimum state for the edges in test_case.csv file using Genetic algorithm


if __name__=='__main__':
    main()