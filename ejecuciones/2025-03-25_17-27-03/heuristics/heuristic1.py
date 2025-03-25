
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes jobs with fewer operations 
    and selects the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}

    # Sort jobs by number of operations (shortest job first)
    job_priority = sorted(jobs_data.keys(), key=lambda job: len(jobs_data[job]))

    for job in job_priority:
        schedule[job] = []
        job_time = 0
        
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines
            best_machine, best_time, best_processing_time = None, float('inf'), None
            for i, machine in enumerate(machines):
                available_time = max(machine_available_time[machine], job_time)
                if available_time < best_time:
                    best_machine, best_time, best_processing_time = machine, available_time, times[i]

            start_time = best_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_time = end_time
            job_completion_time[job] = end_time

    return schedule
