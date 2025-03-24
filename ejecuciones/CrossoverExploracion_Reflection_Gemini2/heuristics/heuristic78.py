
def heuristic(input_data):
    """Heuristic for FJSSP: Random machine assignment with SPT."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    import random

    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job_id]):
            machines = operation[0]
            times = operation[1]

            #Random machine selection
            selected_machine_idx = random.randint(0, len(machines)-1)
            selected_machine = machines[selected_machine_idx]
            processing_time = times[selected_machine_idx]

            start_time = max(machine_available_time[selected_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': selected_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[selected_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
