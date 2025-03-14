def calculate_crowding_distance(front):
    num_ind = len(front)

    for ind in front:
        ind.crowding_distance = 0.0  

    for obj in front[0].evaluation.keys():
        front.sort(key=lambda ind: ind.evaluation[obj])

        front[0].crowding_distance = float("inf")
        front[-1].crowding_distance = float("inf")

        f_min = front[0].evaluation[obj]
        f_max = front[-1].evaluation[obj]
        
        if f_max == f_min:
            continue

        for i in range(1, num_ind - 1):
            front[i].crowding_distance += (front[i + 1].evaluation[obj] - front[i - 1].evaluation[obj]) / (f_max - f_min)