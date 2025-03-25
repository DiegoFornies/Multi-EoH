
def heuristic(input_data):
    """Heuristic for FJSSP: SPT with machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    available_operations = []
    for job_id in jobs:
        available_operations.append((job_id, 1))

    while available_operations:
        best_op = None
        min_end_time = float('inf')

        for job_id, op_num in available_operations:
            machines, times = jobs[job_id][op_num - 1]
            earliest_start_time = float('inf')
            chosen_machine = None
            processing_time=float('inf')

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_time[job_id])
                end_time = start_time + times[m_idx]
                if end_time < min_end_time:
                    min_end_time = end_time
                    earliest_start_time = start_time
                    best_op = (job_id, op_num, m, times[m_idx])
                    chosen_machine = m
                    processing_time = times[m_idx]

        job_id, op_num, assigned_machine, processing_time = best_op
        start_time = max(machine_available_times[assigned_machine], job_completion_time[job_id])

        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({'Operation': op_num, 'Assigned Machine': assigned_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': processing_time})
        machine_available_times[assigned_machine] = end_time
        job_completion_time[job_id] = end_time
        available_operations.remove((job_id, op_num))

        if op_num < len(jobs[job_id]):
            available_operations.append((job_id, op_num + 1))

    return schedule
