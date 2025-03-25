
def heuristic(input_data):
    """
    A heuristic that schedules jobs based on shortest processing time and earliest available machine.
    Prioritizes minimizing makespan by considering machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times

    # Flatten operations for sorting and scheduling
    all_operations = []
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on shortest processing time.
    all_operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in all_operations:
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = times[m_idx]

        start_time = earliest_start_time
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
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
