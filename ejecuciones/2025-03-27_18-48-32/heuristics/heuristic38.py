
def heuristic(input_data):
    """A heuristic for FJSSP using a global optimization approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Precompute all possible operation assignments
    possible_assignments = []
    for job_id in jobs:
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            for i, machine in enumerate(machines):
                possible_assignments.append((job_id, op_idx, machine, times[i]))

    # Sort assignments by processing time (shortest first)
    possible_assignments.sort(key=lambda x: x[3])

    # Greedily assign operations, respecting precedence and machine availability
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    for job_id, op_idx, machine, processing_time in possible_assignments:
        start_time = max(machine_available_times[machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[machine] = end_time
        job_completion_times[job_id] = end_time
    schedule = {k: v for k in schedule if v}
    return schedule
