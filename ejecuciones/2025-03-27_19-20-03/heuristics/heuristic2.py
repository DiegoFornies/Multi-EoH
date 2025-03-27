
def heuristic(input_data):
    """
    A heuristic algorithm for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes shorter processing times and lighter machine loads.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    # Flatten the job operations for easier processing and sorting
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations based on shortest processing time available
    operations.sort(key=lambda x: min(x[3]))  # x[3] is times list

    for job_id, op_num, machines, times in operations:
        best_machine, best_time, earliest_start = None, float('inf'), float('inf')

        # Find the best machine for the operation based on shortest time
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            available_time = machine_load[machine]
            
            # Consider job completion time to ensure sequence feasibility
            start_time = max(available_time, job_completion_times[job_id])
            
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = processing_time
            elif start_time == earliest_start and processing_time < best_time:
                best_machine = machine
                best_time = processing_time
        
        start_time = max(machine_load[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time

        # Update schedule
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
