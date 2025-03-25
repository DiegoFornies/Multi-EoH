
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with the shortest processing time
    and assigns them to the least loaded machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))
    
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine with the earliest available time among possible machines
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = float('inf')

        for m_idx, m in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_load[m], job_completion_times[job])
            
            if start_time < min_start_time or (start_time == min_start_time and processing_time < best_processing_time):
                min_start_time = start_time
                best_machine = m
                best_processing_time = processing_time

        start_time = min_start_time
        end_time = start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
