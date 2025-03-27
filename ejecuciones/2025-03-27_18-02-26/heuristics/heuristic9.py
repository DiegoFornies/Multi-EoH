
def heuristic(input_data):
    """A heuristic for the Flexible Job Shop Scheduling Problem."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort operations based on SPT (Shortest Processing Time)
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # SPT rule: sort operations based on the minimum processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        # Find the machine that results in the earliest completion time
        best_machine = None
        earliest_completion_time = float('inf')

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job])
            completion_time = start_time + processing_time

            if completion_time < earliest_completion_time:
                earliest_completion_time = completion_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time
        
        # Update schedule, machine available time, and job completion time
        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': earliest_completion_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_times[best_machine] = earliest_completion_time
        job_completion_times[job] = earliest_completion_time
        
    return schedule
