
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes operations with shorter processing times and considers machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Flatten operations into a list with job and operation indices.
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_details in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op_details))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_num, op_details in operations:
        machines, times = op_details

        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = times[i]

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
