
def heuristic(input_data):
    """A heuristic that randomly assigns machines to operations."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        job_start_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            # Randomly choose a machine
            chosen_machine_idx = random.randint(0, len(machines) - 1)
            assigned_machine = machines[chosen_machine_idx]
            processing_time = times[chosen_machine_idx]

            start_time = max(machine_available_time[assigned_machine], job_start_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[assigned_machine] = end_time
            job_start_time = end_time

    return schedule
