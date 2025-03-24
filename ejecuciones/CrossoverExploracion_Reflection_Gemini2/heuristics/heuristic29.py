
def heuristic(input_data):
    """
    Heuristic for FJSSP scheduling: Iteratively assigns operations to machines
    based on earliest completion time, considering both machine and job availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations ready to be scheduled. Initially, it contains the first operation of each job.
    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))  # (job_id, operation_index)

    while ready_operations:
        # Sort ready operations by earliest possible start time
        ready_operations.sort(key=lambda x: min(max(machine_available_times[m], job_completion_times[x[0]])
                                                  for m in jobs_data[x[0]][x[1]][0]))

        job_id, op_idx = ready_operations.pop(0)
        machines, times = jobs_data[job_id][op_idx]

        # Find the machine that allows the earliest completion time for this operation
        best_machine, best_time = None, float('inf')
        for m, t in zip(machines, times):
            start_time = max(machine_available_times[m], job_completion_times[job_id])
            completion_time = start_time + t
            if completion_time < best_time:
                best_time = completion_time
                best_machine = m
                best_processing_time = t
                best_start_time = start_time

        machine_available_times[best_machine] = best_time
        job_completion_times[job_id] = best_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_time,
            'Processing Time': best_processing_time
        })

        # Add the next operation of this job to the ready operations, if it exists
        if op_idx + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_idx + 1))
        
    return schedule
