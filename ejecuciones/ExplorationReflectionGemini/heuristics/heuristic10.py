
def heuristic(input_data):
    """
    A heuristic scheduling algorithm for FJSSP that considers machine load
    and job waiting time to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}
    machine_load = {m: 0 for m in range(n_machines)} # Track total processing time on each machine

    # Create a list of operations with job and operation indices for sorting
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        # Find the earliest available machine considering job dependencies
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]

            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        start_time = best_start_time
        end_time = start_time + best_processing_time
        operation_number = op_idx + 1

        schedule[job].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        machine_load[best_machine] += best_processing_time
        

    return schedule
