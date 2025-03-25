
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing machine idle time and 
    job waiting time using a greedy approach, assigning operations to the earliest 
    available machine while respecting precedence constraints.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_assignments = {m: [] for m in range(n_machines)}
    schedule = {}

    for job_id in jobs_data:
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs_data[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            # Assign operation to the best machine
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            machine_assignments[best_machine].append((job_id,op_num))

    return schedule
