
def heuristic(input_data):
    """Prioritizes operations by urgency and machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    unscheduled_operations = []

    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(jobs[job_id])):
            unscheduled_operations.append((job_id, op_idx))

    while unscheduled_operations:
        best_op = None
        earliest_end_time = float('inf')

        for job_id, op_idx in unscheduled_operations:
            machines, times = jobs[job_id][op_idx]
            min_start_time = float('-inf')
            min_end_time = float('inf')
            for i, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + times[i]
                if end_time < min_end_time:
                    min_end_time = end_time
                    selected_machine = machine
                    selected_time = times[i]
                    min_start_time = start_time

            if min_end_time < earliest_end_time:
                earliest_end_time = min_end_time
                best_op = (job_id, op_idx, selected_machine, min_start_time, selected_time)

        job_id, op_idx, machine, start_time, processing_time = best_op
        unscheduled_operations.remove((job_id, op_idx))

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

        machine_available_times[machine] = start_time + processing_time
        job_completion_times[job_id] = start_time + processing_time

    return schedule
