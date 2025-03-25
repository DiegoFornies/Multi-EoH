
def heuristic(input_data):
    """
    Heuristic scheduling algorithm for Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes shorter processing times and machine load balancing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_available_times = {m: 0 for m in range(n_machines)}

    # Create a list of operations and sort it
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    #Custom sorting logic to prioritze operations.
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        #Find the best available machine.
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job])
            end_time = start_time + processing_time
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time

        if job not in schedule:
            schedule[job] = []
        
        start_time = max(machine_available_times[best_machine], job_completion_times[job])
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
