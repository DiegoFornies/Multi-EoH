
def heuristic(input_data):
    """Minimize makespan using machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs[job]):
            operations.append((job, op_idx, machines, times))
    
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_load[machine], job_completion_time[job])
            end_time = start_time + times[m_idx]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = times[m_idx]
                best_start_time = start_time

        machine_load[best_machine] = min_end_time
        job_completion_time[job] = min_end_time
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })
    return schedule
