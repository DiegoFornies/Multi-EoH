
def heuristic(input_data):
    """
    A heuristic for FJSSP: Assigns operations to machines based on the shortest processing time
    and earliest available time, considering both machine and job availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations with their job and operation number
    operations = []
    for job, job_ops in jobs_data.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job, op_idx + 1, op_data))

    # Sort the operations by the sum of their processing times (shortest job first)
    operations.sort(key=lambda x: sum(x[2][1]))  # Sort by sum of processing times


    for job, op_num, op_data in operations:
        machines, times = op_data

        best_machine, best_time = None, float('inf')
        earliest_start = float('inf')

        # Find the best machine for the operation
        for i, machine in enumerate(machines):
            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job])

            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = times[i]


        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time

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
