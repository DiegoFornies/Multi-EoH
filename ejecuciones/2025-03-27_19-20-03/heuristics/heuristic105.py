
def heuristic(input_data):
    """Greedy heuristic: Prioritize operations based on earliest end time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    available_ops = []
    for job in jobs:
        available_ops.append((job, 0))  # (job_id, op_index)

    while available_ops:
        best_op = None
        best_machine = None
        earliest_end_time = float('inf')

        for job, op_idx in available_ops:
            machines, times = jobs[job][op_idx]

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_op = (job, op_idx)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job, op_idx = best_op
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': earliest_end_time,
            'Processing Time': best_processing_time
        })

        machine_time[best_machine] = earliest_end_time
        job_completion_time[job] = earliest_end_time

        available_ops.remove((job, op_idx))

        op_idx += 1
        if op_idx < len(jobs[job]):
            available_ops.append((job, op_idx))

    return schedule
