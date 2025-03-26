
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).

    Key Idea: Prioritizes operations with shorter processing times on less loaded machines to balance machine utilization and reduce makespan.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations, sorted by shortest processing time first
    all_operations = []
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append((job, op_idx, machines, times))

    # Custom Sort based on processing time
    all_operations.sort(key=lambda x: min(x[3]))
    
    for job, op_idx, machines, times in all_operations:
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time

        # Assign the operation to the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time
    
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
