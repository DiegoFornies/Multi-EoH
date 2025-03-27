
def heuristic(input_data):
    """FJSSP heuristic: Random machine assignment with job precedence."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            # Randomly choose a machine from the available options
            best_machine = random.choice(possible_machines)
            processing_time = possible_times[possible_machines.index(best_machine)]

            # Ensure job precedence
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id] if op_idx > 0 else 0)

            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            current_time = end_time

    return schedule
