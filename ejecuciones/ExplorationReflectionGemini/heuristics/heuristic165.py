
def heuristic(input_data):
    """Combines load balancing with SPT for FJSSP. Balances makespan & separation."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    job_remaining_times = {}
    for job_id in range(1, n_jobs + 1):
        total_time = 0
        for machines, times in jobs[job_id]:
            total_time += min(times)
        job_remaining_times[job_id] = total_time

    jobs_order = sorted(range(1, n_jobs + 1), key=lambda x: job_remaining_times[x])

    for job_id in jobs_order:
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_end_time = float('inf')

            for machine_index, machine in enumerate(possible_machines):
                processing_time = possible_times[machine_index]

                start_time = max(machine_load[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_load[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
        job_remaining_times[job_id] = 0

    return schedule
