
def heuristic(input_data):
    """
    A heuristic to solve the Flexible Job Shop Scheduling Problem.

    This heuristic prioritizes operations with shorter processing times
    and assigns them to machines that become available earlier.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times
    
    # Create a list of operations with job, operation index, machines, and times
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on the minimum processing time across available machines
    operations.sort(key=lambda x: min(x[3]))  # Prioritize shorter operations
    
    for job, op_num, machines, times in operations:
        best_machine, best_time, best_start = None, float('inf'), None

        # Find the best machine (earliest available time) for the current operation
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            
            if start_time < best_time:
                best_machine, best_time, best_start = machine, start_time, start_time

        if best_machine is None:
            # If no suitable machine is found, skip the operation (should not happen in a valid instance)
            continue

        processing_time = times[machines.index(best_machine)]
        end_time = best_start + processing_time

        # Update schedule information
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
