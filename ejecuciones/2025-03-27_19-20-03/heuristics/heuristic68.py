
def heuristic(input_data):
    """FJSSP heuristic: Random machine assignment with earliest start time."""
    import random
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_index in range(len(jobs_data[job_id])):
            machines, times = jobs_data[job_id][op_index]

            # Randomly select a machine from the available options.
            machine_index = random.randint(0, len(machines) - 1)
            assigned_machine = machines[machine_index]
            processing_time = times[machine_index]

            # Calculate the earliest possible start time.
            start_time = max(machine_available_time[assigned_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            # Update the schedule and machine/job completion times.
            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[assigned_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
