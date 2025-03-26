
def heuristic(input_data):
    """A heuristic that schedules operations based on shortest processing time (SPT) first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    operations = []
    for job_id in jobs:
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            min_time = float('inf')
            best_machine = None
            for i in range(len(machines)):
                if times[i] < min_time:
                    min_time = times[i]
                    best_machine = machines[i]
            operations.append((min_time, job_id, op_idx, best_machine))

    operations.sort()

    for op in operations:
        processing_time, job_id, op_idx, machine = op
        op_num = op_idx + 1
        start_time = max(machine_available_times[machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
             schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
