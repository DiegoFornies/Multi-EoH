
def heuristic(input_data):
    """FJSSP heuristic: Random machine assignment with earliest start."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_index, operation in enumerate(operations):
            eligible_machines = operation[0]
            processing_times = operation[1]

            # Randomly choose a machine.
            import random
            machine_index = random.randint(0, len(eligible_machines) - 1)
            best_machine = eligible_machines[machine_index]
            best_processing_time = processing_times[machine_index]

            start_time = max(machine_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
