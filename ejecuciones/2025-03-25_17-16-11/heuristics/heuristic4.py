
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine availability and job completion time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations sorted by the shortest processing time among possible machines
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            machines, times = op_data
            min_time = min(times)
            operations.append((min_time, job_id, op_idx, machines, times))

    operations.sort()  # Sort by shortest processing time

    for _, job_id, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine that allows the earliest start time
        best_machine = None
        earliest_start_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_time = times[i]
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
