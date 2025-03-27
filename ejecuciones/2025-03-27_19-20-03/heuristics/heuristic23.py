
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes shortest processing time and earliest machine availability
    to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    operations = []  # (job_id, operation_index)
    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(jobs_data[job_id])):
            operations.append((job_id, op_idx))

    # Sort operations by shortest processing time on the first available machine
    operations.sort(key=lambda op: min(jobs_data[op[0]][op[1]][1]))

    for job_id, op_idx in operations:
        machines = jobs_data[job_id][op_idx][0]
        times = jobs_data[job_id][op_idx][1]

        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None
        
        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]

            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time


        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time
        op_num = op_idx + 1


        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

    return schedule
