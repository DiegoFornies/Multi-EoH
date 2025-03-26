
def heuristic(input_data):
    """Schedules jobs using Shortest Processing Time (SPT) with machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times, job))

    # Sort operations by shortest processing time among available machines, job number, operation index
    operations.sort(key=lambda x: (min(x[3]), x[4], x[1]))

    for job, op_idx, machines, times, job_id in operations:
        op_num = op_idx + 1
        # Choose machine with earliest availability for SPT operation
        best_machine = None
        min_start_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_time[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = times[i]

        end_time = min_start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': min_start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
