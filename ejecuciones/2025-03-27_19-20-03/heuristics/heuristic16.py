
def heuristic(input_data):
    """
    Heuristic for FJSSP. Minimizes makespan by prioritizing operations
    with shortest processing time across available machines for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    operations = []  # List of (job, op_idx) tuples to schedule
    for job, operations_list in jobs_data.items():
        for op_idx in range(len(operations_list)):
            operations.append((job, op_idx))

    # Prioritize operations based on shortest processing time across available machines
    operations.sort(key=lambda item: min(input_data['jobs'][item[0]][item[1]][1]))

    for job, op_idx in operations:
        machines, times = jobs_data[job][op_idx]
        
        # Find the machine that allows the earliest completion time for this operation
        best_machine, min_completion_time = None, float('inf')
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            completion_time = start_time + processing_time

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        if job not in schedule:
            schedule[job] = []

        op_num = op_idx + 1  # Operation number within the job

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_completion_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = min_completion_time
        job_completion_time[job] = min_completion_time
    
    return schedule
