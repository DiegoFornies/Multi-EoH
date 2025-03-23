
def heuristic(input_data):
    """Schedules jobs to minimize makespan, balancing load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    ready_operations = []
    for job_id in jobs:
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        earliest_start_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs[job_id][op_index]
            min_start_time = float('inf')

            for machine_id, processing_time in zip(machines, times):
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])
                min_start_time = min(min_start_time, start_time)

            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_job, best_op_index = job_id, op_index

        job_id, op_index = best_job, best_op_index
        machines, times = jobs[job_id][op_index]

        best_machine, best_processing_time = None, float('inf')
        earliest_completion_time = float('inf')

        for machine_id, processing_time in zip(machines, times):
            start_time = max(machine_available_time[machine_id], job_completion_time[job_id])
            completion_time = start_time + processing_time

            if completion_time < earliest_completion_time:
                earliest_completion_time = completion_time
                best_machine, best_processing_time = machine_id, processing_time

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
