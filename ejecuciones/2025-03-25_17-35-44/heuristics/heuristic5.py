
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with shorter processing times
    and balances machine load to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of operations with job and operation indices
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))
            
    # Sort operations based on shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time
        
        if best_machine is None:
            #If there is not feasible machine. Break the loop.
            return {}

        start_time = earliest_start_time
        end_time = start_time + best_processing_time
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

        # Update the schedule
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

    return schedule
