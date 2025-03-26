
def heuristic(input_data):
    """Schedules jobs balancing makespan and machine load, considering job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_remaining_times = {}

    for job_id in range(1, n_jobs + 1):
        remaining_time = 0
        for machines, times in jobs[job_id]:
            remaining_time += min(times)
        job_remaining_times[job_id] = remaining_time

    for job_id in range(1, n_jobs + 1):
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_weighted_time = float('inf')

            # Prioritize machines with lower load, then job urgency
            for machine_index, machine in enumerate(possible_machines):
                processing_time = possible_times[machine_index]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                # Weighting function: considers machine load and job urgency.
                weighted_time = end_time + 0.1 * machine_available_times[machine] - 0.05 * job_remaining_times[job_id]

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time
            job_remaining_times[job_id] -= best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
    return schedule
