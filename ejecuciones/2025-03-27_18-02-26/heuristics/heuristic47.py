
def heuristic(input_data):
    """FJSSP heuristic: Random machine assignment."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    import random

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, operation in enumerate(operations):
            machines, times = operation

            # Randomly select a machine.
            chosen_machine_index = random.randint(0, len(machines) - 1)
            chosen_machine = machines[chosen_machine_index]
            processing_time = times[chosen_machine_index]

            start_time = max(machine_available_time[chosen_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': chosen_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[chosen_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
