
def heuristic(input_data):
    """Schedules jobs based on dynamic operation criticality and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    remaining_job_times = {}

    # Initialize remaining job times
    for job_id in range(1, n_jobs + 1):
        remaining_job_times[job_id] = sum(sum(op[1]) / len(op[1]) for op in jobs[job_id])

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    scheduled_operations = 0
    total_operations = sum(len(jobs[j]) for j in range(1, n_jobs + 1))

    while scheduled_operations < total_operations:
        eligible_operations = []
        for job_id in range(1, n_jobs + 1):
            if len(schedule[job_id]) < len(jobs[job_id]):
                next_operation_index = len(schedule[job_id])
                eligible_operations.append((job_id, next_operation_index))

        best_operation = None
        best_machine = None
        min_weighted_time = float('inf')

        for job_id, operation_index in eligible_operations:
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Calculate criticality: remaining time / current completion
            criticality = remaining_job_times[job_id] / (job_completion_times[job_id] + 1e-6)

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                # Weighted time: considers load, criticality, and processing time
                weighted_time = end_time + 0.1 * machine_available_times[machine] - 0.2 * criticality # Load, critical

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_operation = (job_id, operation_index)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        if best_operation is not None:
            job_id, operation_index = best_operation
            machine = best_machine

            machine_available_times[machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            remaining_job_times[job_id] -= best_processing_time
            scheduled_operations += 1

        else:
          # Handle edge case if no operation is eligible
          break

    return schedule
