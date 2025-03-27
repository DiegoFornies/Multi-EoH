
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time and balancing machine load.
    Chooses the machine that results in the earliest completion time for the operation,
    considering both machine availability and job completion time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            op_num = op_idx + 1
            
            best_machine = None
            earliest_end_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_time = time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': earliest_end_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = earliest_end_time
            job_completion_time[job] = earliest_end_time

    return schedule
