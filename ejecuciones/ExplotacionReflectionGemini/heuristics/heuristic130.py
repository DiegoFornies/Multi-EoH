
def heuristic(input_data):
    """Combines shortest processing time and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    while available_operations:
        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs_data[job_id][op_idx]

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, start_time, processing_time)
                elif end_time == min_end_time:
                    if machine_load[machine] < machine_load[best_machine[0]]:
                        best_operation = (job_id, op_idx)
                        best_machine = (machine, start_time, processing_time)

        job_id, op_idx = best_operation
        machine, start_time, processing_time = best_machine

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = start_time + processing_time
        job_completion_time[job_id] = start_time + processing_time
        machine_load[machine] += processing_time
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs_data[job_id]):
            available_operations.append((job_id, op_idx + 1))

    return schedule
