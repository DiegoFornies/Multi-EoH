
def heuristic(input_data):
    """Schedules jobs minimizing makespan by prioritizing operations with fewer machine options."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Corrected job indexing

    # Create a list of operations with job and operation indices
    operations = []
    for job_id, operations_list in jobs.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations based on the number of available machines (prioritize smaller choices)
    operations.sort(key=lambda x: len(x[2]))  # Sort by the number of machines

    for job_id, op_num, machines, times in operations:
        # Find the earliest available time on a suitable machine
        best_machine = None
        min_start_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            available_time = max(machine_available_time[machine], job_completion_time[job_id])
            if available_time < min_start_time:
                min_start_time = available_time
                best_machine = machine
                processing_time = times[i]
            
        # If no machine is available (should not happen, but handle it)
        if best_machine is None:
            best_machine = machines[0]
            processing_time = times[0]
            min_start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            
        start_time = min_start_time
        end_time = start_time + processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
    return schedule
