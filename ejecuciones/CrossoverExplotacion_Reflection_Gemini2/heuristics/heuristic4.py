
def heuristic(input_data):
    """Schedules jobs on machines minimizing makespan, idle time, and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Sort operations by shortest processing time
    operations = []
    for job_id, operations_list in jobs.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job_id, op_idx + 1, machines, times))

    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_num, machines, times in operations:
        best_machine, best_time, earliest_start = -1, float('inf'), float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            available_time = machine_available_times[machine]
            job_ready_time = job_completion_times[job_id]
            start_time = max(available_time, job_ready_time)

            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = processing_time

        start_time = earliest_start
        end_time = start_time + best_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
