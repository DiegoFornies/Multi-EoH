
def heuristic(input_data):
    """Schedules jobs with earliest finish time heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_loads = {m: 0 for m in range(n_machines)}

    schedule = {}
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx, op_data))

    # Sort operations using SPT (Shortest Processing Time) based on minimal processing time on available machines.
    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_idx, op_data in operations:
        machines, times = op_data

        # Find the earliest possible start time for the operation
        best_machine, min_start_time, min_processing_time = None, float('inf'), None
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                min_processing_time = times[m_idx] # select processing time based on the machine selected

        start_time = min_start_time
        end_time = start_time + min_processing_time
        processing_time = min_processing_time
        assigned_machine = best_machine

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[assigned_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_loads[assigned_machine] += processing_time

    return schedule
