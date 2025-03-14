import numpy as np

def calculate_distances_to_reference_vectors(population, reference_vectors): #añade en el atributo vector_distance de cada indidivuo sus distancias
    
    for individual in population:
        individual_evaluation = list(individual.evaluation.values())
        individual.vector_distance = {}        
        for reference in reference_vectors:
            distance = np.linalg.norm(np.array(individual_evaluation) - np.array(reference))
            individual.vector_distance[reference] = distance