
def heuristic(input_data):
    """
    Heuristic for FJSSP using shortest processing time and earliest available machine.
    Prioritizes operations with shorter processing times and assigns them to the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    # Create a list of operations with job and operation indices for sorting
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_idx, op_data in enumerate(operations_list):
            operations.append((job_id, op_idx, op_data))

    # Sort operations by shortest processing time across available machines
    operations.sort(key=lambda x: min(x[2][1]))  # Sort by min processing time

    for job_id, op_idx, op_data in operations:
        machines, times = op_data
        
        # Find the earliest available machine among the feasible ones
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = 0

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = time
                
        if best_machine is None:
            print("Error")

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
    
    return schedule
