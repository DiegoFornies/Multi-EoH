
def heuristic(input_data):
    """Schedules jobs, balancing makespan and machine load using a randomized approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    import random

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Randomized Machine Selection
            possible_machines = []
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = max(machine_available_time[machine], job_completion_time)
                end_time = available_time + processing_time
                possible_machines.append((machine, available_time, end_time, processing_time))

            # Sort possible machine based on available time
            possible_machines.sort(key=lambda x: x[1])

            # Apply a probabilistic choice favoring machines with lower loads but with an element of randomness
            probabilities = []
            total_load = sum(machine_load.values())
            if total_load == 0:
                probabilities = [1.0 / len(possible_machines)] * len(possible_machines)
            else:
                for machine, _, _, _ in possible_machines:
                    load_factor = 1.0 - (machine_load[machine] / total_load)
                    probabilities.append(load_factor)

                # Normalize the probabilities
                sum_probabilities = sum(probabilities)
                probabilities = [p / sum_probabilities for p in probabilities]
            
            chosen_index = random.choices(range(len(possible_machines)), weights=probabilities, k=1)[0]
            best_machine, best_start_time, best_end_time, best_processing_time = possible_machines[chosen_index]


            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time = best_end_time

    return schedule
