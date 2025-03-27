
def heuristic(input_data):
    """Heuristic for FJSSP: Random machine selection."""
    import random
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Randomly choose a machine from the available options.
            chosen_machine_index = random.randint(0, len(machines) - 1)
            best_machine = machines[chosen_machine_index]
            processing_time = times[chosen_machine_index]

            available_time = max(machine_available_time[best_machine], job_completion_time)
            start_time = available_time
            end_time = start_time + processing_time
            
            # Schedule the operation
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            
            # Update machine available time and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time = end_time
    
    return schedule
