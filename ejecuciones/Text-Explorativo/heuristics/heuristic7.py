
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem.
    Prioritizes operations with shortest processing time on least loaded machines.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations with job number, op index, machines, and processing times
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_index, (machines, times) in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_index': op_index,
                'machines': machines,
                'times': times
            })

    # Sort operations based on shortest processing time
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job_id = operation['job_id']
        op_index = operation['op_index']
        machines = operation['machines']
        times = operation['times']

        # Find the least loaded machine available for this operation
        available_machines = []
        for i, machine in enumerate(machines):
            available_machines.append((machine, times[i], max(machine_availability[machine], job_completion_time[job_id])))

        # Sort available machines based on the earliest possible start time (machine_availability or job_completion_time, whichever is later)
        available_machines.sort(key=lambda x: x[2] + x[1])

        best_machine = available_machines[0][0]
        best_time = available_machines[0][1]
        start_time = available_machines[0][2]

        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] += best_time
        machine_availability[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
