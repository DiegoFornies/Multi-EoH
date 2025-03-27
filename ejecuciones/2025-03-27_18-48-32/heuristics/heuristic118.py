
def heuristic(input_data):
    """Schedules jobs by minimizing idle time and balancing machine load using a modified Shortest Processing Time (SPT) rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(n_jobs + 1)}

    for job_id in jobs:
        schedule[job_id] = []

    remaining_operations = {job_id: list(range(len(jobs[job_id]))) for job_id in jobs}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job_id, operations in remaining_operations.items():
            if operations:
                op_idx = operations[0]
                machines = jobs[job_id][op_idx][0]
                times = jobs[job_id][op_idx][1]

                min_time = float('inf')
                for time in times:
                    min_time = min(min_time, time)

                eligible_operations.append((min_time, job_id, op_idx, machines, times))

        eligible_operations.sort(key=lambda x: x[0])  # SPT rule

        _, job_id, op_idx, machines, times = eligible_operations[0]

        best_machine = None
        min_finish_time = float('inf')

        for i, machine_id in enumerate(machines):
            start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
            finish_time = start_time + times[i]
            if finish_time < min_finish_time:
                min_finish_time = finish_time
                best_machine = machine_id
                processing_time = times[i]

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        remaining_operations[job_id].pop(0)
    return schedule
