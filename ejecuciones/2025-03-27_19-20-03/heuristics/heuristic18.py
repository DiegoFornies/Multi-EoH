
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing idle time
    and balancing machine load by selecting the machine with the
    earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, operation in enumerate(operations):
            op_num = op_idx + 1
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            earliest_start_time = float('inf')

            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine_id
                    best_processing_time = processing_time

            start_time = earliest_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
