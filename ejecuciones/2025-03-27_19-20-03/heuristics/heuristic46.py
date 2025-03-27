
def heuristic(input_data):
    """FJSSP heuristic: Random machine selection with makespan consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    import random
    
    for job in jobs:
        schedule[job] = []
        for op_idx in range(len(jobs[job])):
            machines, times = jobs[job][op_idx]
            
            # Randomly select a machine from the available options
            chosen_machine_index = random.randint(0, len(machines) - 1)
            best_machine = machines[chosen_machine_index]
            best_time = times[chosen_machine_index]

            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + best_time
            
            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })
            
            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
