
def heuristic(input_data):
    """Hybrid heuristic: SPT-based job scheduling with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_remaining_times = {}

    for job_id in range(1, n_jobs + 1):
        remaining_time = 0
        for machines, times in jobs[job_id]:
            remaining_time += min(times)
        job_remaining_times[job_id] = remaining_time

    job_priorities = {j: job_remaining_times[j] for j in range(1, n_jobs + 1)}
    sorted_jobs = sorted(range(1, n_jobs + 1), key=lambda x: job_priorities[x])

    for job_id in sorted_jobs:
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for machine_index, machine in enumerate(possible_machines):
                processing_time = possible_times[machine_index]
                start_time = max(machine_load[machine], job_completion_times[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_load[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
