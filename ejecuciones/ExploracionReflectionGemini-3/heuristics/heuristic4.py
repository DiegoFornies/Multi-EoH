
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with the shortest processing time
    and assigns them to the least loaded machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of all operations, including job and operation indices
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time (first available machine)
    operations.sort(key=lambda x: x[3][0])  # Sort by the first available machine's processing time

    for job, op_num, machines, times in operations:
        # Find the earliest available machine for this operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for i, machine in enumerate(machines):
            start_time = max(machine_load[machine], job_completion_times[job])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = times[i]
        
        # If this job isn't in the schedule, initialize the schedule
        if job not in schedule:
            schedule[job] = []

        # Add the operation to the schedule
        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
