
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    operations_ready = {j: 0 for j in range(1, n_jobs + 1)}

    while True:
        eligible_operations = []
        for job_id in range(1, n_jobs + 1):
            if operations_ready[job_id] < len(jobs[job_id]):
                eligible_operations.append(job_id)

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        min_combined_score = float('inf')

        for job_id in eligible_operations:
            op_index = operations_ready[job_id]
            possible_machines = jobs[job_id][op_index][0]
            possible_times = jobs[job_id][op_index][1]

            for machine_index, machine in enumerate(possible_machines):
                processing_time = possible_times[machine_index]
                start_time = max(machine_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Combined score (makespan + machine load)
                combined_score = end_time + 0.1 * machine_time[machine]
                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_operation = job_id
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        op_index = operations_ready[best_operation]
        machine_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[best_operation] = best_start_time + best_processing_time

        schedule[best_operation].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })
        operations_ready[best_operation] += 1

    return schedule
