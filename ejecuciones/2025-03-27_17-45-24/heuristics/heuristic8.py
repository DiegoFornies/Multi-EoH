
def heuristic(input_data):
    """Schedules jobs using a greedy approach, minimizing idle time and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the earliest available time AND least load from feasible machines
            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time)
                end_time = start_time + times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_time = times[m_idx]

            # Assign the operation to the best machine
            start_time = max(machine_time[best_machine], job_completion_time)
            end_time = start_time + best_time
            schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': best_time})

            # Update machine time and job completion time
            machine_time[best_machine] = end_time
            machine_load[best_machine] += best_time
            job_completion_time = end_time
    
    return schedule
