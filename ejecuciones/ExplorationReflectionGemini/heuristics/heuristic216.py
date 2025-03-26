
def heuristic(input_data):
    """Uses a random machine assignment for each operation."""
    import random
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
            
            # Randomly select a machine
            chosen_machine_index = random.randint(0, len(possible_machines) - 1)
            chosen_machine = possible_machines[chosen_machine_index]
            processing_time = possible_times[chosen_machine_index]

            start_time = max(machine_available_times[chosen_machine], job_completion_times[job_id])
            end_time = start_time + processing_time
            
            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': chosen_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[chosen_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
