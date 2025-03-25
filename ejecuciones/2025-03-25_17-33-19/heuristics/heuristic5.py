
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with fewer machine choices
    and shorter processing times to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with their job and operation number
    operations = []
    for job, ops in jobs_data.items():
        for i, op in enumerate(ops):
            operations.append((job, i + 1, op))

    # Sort operations based on the number of available machines and processing time (shortest first)
    operations.sort(key=lambda x: (len(x[2][0]), min(x[2][1])))

    for job, op_num, op_data in operations:
        machines, times = op_data
        best_machine, best_time = None, float('inf')

        # Find the earliest available machine
        for i, machine in enumerate(machines):
            if times[i] < best_time:
                best_machine, best_time = machine, times[i]

        # Schedule the operation on the best available machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
