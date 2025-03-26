
def heuristic(input_data):
    """Schedule jobs minimizing makespan with lookahead."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_end_time = float('inf')

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                # Lookahead: Consider the impact on the next operation.
                next_op_end_time = 0
                if operation_index + 1 < len(job_operations):
                    next_operation_data = job_operations[operation_index + 1]
                    next_possible_machines = next_operation_data[0]
                    next_possible_times = next_operation_data[1]

                    min_next_end_time = float('inf')
                    for j in range(len(next_possible_machines)):
                        next_machine = next_possible_machines[j]
                        next_processing_time = next_possible_times[j]
                        next_start_time = max(machine_available_times[next_machine], end_time) # next op cannot start until this one completes.
                        next_end_time_candidate = next_start_time + next_processing_time
                        min_next_end_time = min(min_next_end_time, next_end_time_candidate)
                    
                    next_op_end_time = min_next_end_time

                # Choose machine that minimizes the end time + impact to the next operation
                if end_time + 0.1 * next_op_end_time < min_end_time:
                    min_end_time = end_time + 0.1 * next_op_end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
