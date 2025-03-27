
def heuristic(input_data):
    """A heuristic for FJSSP that minimizes makespan,
    prioritizing operations with fewer machine choices."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations, sorted by the number of possible machines
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((len(machines), job_id, op_idx, machines, times))  # (priority, job_id, op_idx, machines, times)
    operations.sort(key=lambda x: x[0])

    for _, job_id, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        # Find the earliest available time for this operation on any suitable machine
        best_machine = None
        earliest_start = float('inf')
        processing_time = None
        
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                processing_time = times[m_idx] #select processing time based on machine

        # Schedule the operation on the best machine
        if job_id not in schedule:
            schedule[job_id] = []

        start_time = earliest_start
        end_time = start_time + processing_time

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
