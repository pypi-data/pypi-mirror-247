import random
import math

class GA:
    def __init__(self, individualSize, populationSize):
        self.population = dict()
        self.individualSize = individualSize
        self.populationSize = populationSize
        self.totalFitness = 0
        i = 0
        while i < populationSize:
            listOfBits = [0] * individualSize
            listOfLocations = list(range(0, individualSize))
            numberOfOnes = random.randint(0, individualSize - 1)
            onesLocations = random.sample(listOfLocations, numberOfOnes)
            for j in onesLocations:
                listOfBits[j] = 1
            self.population[i] = [listOfBits, numberOfOnes]
            self.totalFitness = self.totalFitness + numberOfOnes
            i = i + 1

    def updatePopulationFitness(self):
        self.totalFitness = 0
        for individual in self.population:
            individualFitness = sum(self.population[individual][0])
            self.population[individual][1] = individualFitness
            self.totalFitness = self.totalFitness + individualFitness

    def selectParents(self):
        rouletteWheel = []
        h_n = []
        wheelsize = self.populationSize * 5
        for individual in self.population:
            j = 0
            h_n.append(self.population[individual][1])
        for individual in self.population:
            individualLength = round(wheelsize * (h_n[j] / sum(h_n)))
            j = j + 1
            if individualLength > 0:
                i = 0
                while i < individualLength:
                    rouletteWheel.append(individual)
                    i = i + 1
        random.shuffle(rouletteWheel)
        parentIndices = []
        i = 0
        while i < self.populationSize:
            parentIndices.append(rouletteWheel[random.randint(0, len(rouletteWheel) - 1)])
            i = i + 1
        newGeneration = dict()
        i = 0
        while i < self.populationSize:
            newGeneration[i] = self.population[parentIndices[i]].copy()
            i = i + 1
        del self.population
        self.population = newGeneration.copy()
        self.updatePopulationFitness()

    def generateChildren(self, crossoverProbability):
        numberOfPairs = round(crossoverProbability * self.populationSize / 2)
        individualIndices = list(range(0, self.populationSize))
        random.shuffle(individualIndices)
        i = 0
        j = 0
        while i < numberOfPairs:
            crossoverPoint = random.randint(0, self.individualSize - 1)
            child1 = self.population[j][0][0:crossoverPoint] + self.population[j + 1][0][crossoverPoint:]
            child2 = self.population[j + 1][0][0:crossoverPoint] + self.population[j][0][crossoverPoint:]
            self.population[j] = [child1, sum(child1)]
            self.population[j + 1] = [child2, sum(child2)]
            i = i + 1
            j = j + 2
        self.updatePopulationFitness()

    def mutateChildren(self, mutationProbability):
        numberOfBits = round(mutationProbability * self.populationSize * self.individualSize)
        totalIndices = list(range(0, self.populationSize * self.individualSize))
        random.shuffle(totalIndices)
        swapLocations = random.sample(totalIndices, numberOfBits)
        for loc in swapLocations:
            individualIndex = math.floor(loc / self.individualSize)
            bitIndex = loc % self.individualSize
            if self.population[individualIndex][0][bitIndex] == 0:
                self.population[individualIndex][0][bitIndex] = 1
            else:
                self.population[individualIndex][0][bitIndex] = 0
        self.updatePopulationFitness()

def binary_to_decimal(binary_list):
    binary_str = ''.join(map(str, binary_list))
    decimal_value = int(binary_str, 2)
    return decimal_value

def fitness_function(x):
    return -(2 * x**2 + 5)

individualSize, populationSize = 8, 10
i = 0
instance = GA(individualSize, populationSize)

while True:
    instance.selectParents()
    instance.generateChildren(0.8)
    instance.mutateChildren(0.03)

    best_individual = max(instance.population, key=lambda k: instance.population[k][1])
    best_chromosome_decimal = binary_to_decimal(instance.population[best_individual][0])

    print(f"Generation {i}: Best Chromosome Decimal Value: {best_chromosome_decimal}")
    i = i + 1

    if instance.population[best_individual][1] == individualSize:
        break
