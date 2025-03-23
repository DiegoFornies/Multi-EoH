
def heuristic(input_data):
    """Schedules jobs using a combination of earliest finish time, SPT, and machine load, but incorporates a probabilistic element to choose machines."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1

            potential_machines = []
            potential_times = []
            potential_start_times = []
            potential_weighted_finishes = []

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                finish_time = start_time + time
                weighted_finish = 0.6 * finish_time + 0.2 * machine_load[machine] + 0.2 * time # blend finish_time, load, SPT

                potential_machines.append(machine)
                potential_times.append(time)
                potential_start_times.append(start_time)
                potential_weighted_finishes.append(weighted_finish)
            
            # Select machine based on probability distribution of weighted finish times
            import random
            
            # Convert weighted finishes to probabilities using inverse scaling. Add small number to avoid zero and division by zero
            total_weighted_finish = sum(potential_weighted_finishes) + 0.0001
            probabilities = [(total_weighted_finish - wf) / total_weighted_finish for wf in potential_weighted_finishes]
            # Normalize probabilities
            total_prob = sum(probabilities)
            probabilities = [p / total_prob for p in probabilities]

            # Choose the machine
            chosen_index = random.choices(range(len(potential_machines)), weights=probabilities, k=1)[0]

            best_machine = potential_machines[chosen_index]
            best_time = potential_times[chosen_index]
            start_time = potential_start_times[chosen_index]
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += best_time

    return schedule
