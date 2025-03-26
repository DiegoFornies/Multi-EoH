
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with shorter processing times and lower machine load, 
    aiming to minimize makespan and balance machine utilization.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Create a list of all operations with job and operation indices
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on shortest processing time first
    operations.sort(key=lambda x: min(x[3]))  # Prioritize shorter operations

    # Schedule each operation
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        earliest_start_time = float('inf')
        
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_time = times[i]

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
