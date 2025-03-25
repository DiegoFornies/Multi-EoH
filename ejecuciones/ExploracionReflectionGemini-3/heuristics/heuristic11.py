
def heuristic(input_data):
    """
    A heuristic for the FJSSP aiming to minimize makespan by prioritizing
    operations with the shortest processing time on the least loaded machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in jobs_data}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}

    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on the shortest processing time
    operations.sort(key=lambda op: min(op[3]))

    for job, op_num, machines, times in operations:
        best_machine, min_end_time = None, float('inf')
        processing_time = None

        # Find the machine that results in the earliest completion time for the operation
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
