
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritizes operations based on shortest processing time and earliest machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations with job and operation indices
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on shortest processing time (SPT) among available machines
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        best_machine, best_time = -1, float('inf')

        # Find the best machine based on earliest available time and shortest processing time
        for m_idx, m in enumerate(machines):
            if times[m_idx] < best_time and machine_available_time[m] <= best_time:
                best_machine, best_time = m, times[m_idx]

        # Ensure job's previous operation is finished before starting this one.
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
