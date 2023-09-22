import random

def generatePopulation(length):
    return [[random.randrange(0, 1000) for gene in range(100)] for entity in range(int(length))]

def selectThirtyEight(population):
    populationIndex = []

    for index in range(38):
        while True:
            randomIndex = random.randrange(0, len(population))
            if randomIndex not in populationIndex:
                populationIndex.append(randomIndex)
                break

    return populationIndex

def breed(firstEntity, secondEntity):
    indexValues = [g for g in range(100)]
    random.shuffle(indexValues)

    daughterEntity = []

    for gene in range(50):
        daughterEntity.append(firstEntity[indexValues[gene]])
        daughterEntity.append(secondEntity[indexValues[50 + gene]])

    return daughterEntity

def orderSurvivability(civilisation):
    indexedCiv = [(sum(civilisation[entity]), civilisation[entity]) for entity in range(len(civilisation))]
    sortedCiv = sorted(indexedCiv, key=lambda x: x[0], reverse=True)
    zippedObject1, zippedObject2 = zip(*sortedCiv)
    return zippedObject2

def removeEight(civilisation):
    return civilisation[8:]

civilisation = generatePopulation(1000)
for generation in range(150):
    thirtyEightBreeders = [civilisation[breederIndex] for breederIndex in selectThirtyEight(civilisation)]
    bredEntities = [breed(thirtyEightBreeders[x], thirtyEightBreeders[19 + x]) for x in range(19)]
    civilisation = list(list(civilisation) + list(bredEntities))
    civilisation = orderSurvivability(civilisation)
    civilisation = removeEight(civilisation)
    print("generation complete.")
    print("success:", sum([sum(x) for x in civilisation])/len(civilisation))

print(len(civilisation))