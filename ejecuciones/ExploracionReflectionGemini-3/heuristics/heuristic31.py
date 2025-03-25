
def heuristic(input_data):
    """Heuristic for FJSSP scheduling using shortest processing time and earliest available machine."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op_data))  # (job_id, op_num, (machines, times))

    operations.sort(key=lambda x: min(x[2][1]))  # Sort operations by shortest processing time

    for job_id, op_num, op_data in operations:
        machines, times = op_data
        best_machine, best_time = None, float('inf')

        for i, machine in enumerate(machines):
            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job_id])

            if start_time + times[i] < best_time:
                best_machine = machine
                best_time = start_time + times[i]
                processing_time = times[i]
                assigned_start_time = start_time

        machine_available_time[best_machine] = best_time
        job_completion_time[job_id] = best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': assigned_start_time,
            'End Time': best_time,
            'Processing Time': processing_time
        })

    return schedule
