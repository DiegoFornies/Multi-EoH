
def heuristic(input_data):
    """Minimize makespan using a random assignment."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    import random

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        current_time = 0
        for op_idx, op_data in enumerate(jobs[job]):
            machines = op_data[0]
            times = op_data[1]

            # Randomly select a machine.
            chosen_machine_idx = random.randint(0, len(machines) - 1)
            chosen_machine = machines[chosen_machine_idx]
            processing_time = times[chosen_machine_idx]

            start_time = max(machine_time[chosen_machine], current_time)
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': chosen_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[chosen_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
