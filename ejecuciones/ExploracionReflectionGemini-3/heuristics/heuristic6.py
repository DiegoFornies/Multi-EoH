
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) using a shortest processing time and earliest available machine strategy.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Flatten operations for sorting
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))
    
    #Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        # Find the machine that can process the operation the earliest
        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = time

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
    
    return schedule
