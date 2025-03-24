
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations with the fewest machine options and shortest processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}

    # Create a list of operations, sorted by job and operation number
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append({
                'job': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })

    # Sort operations: prioritize those with fewer machine choices and smaller processing times.
    operations.sort(key=lambda x: (len(x['machines']), min(x['times'])))

    while operations:
        best_op = None
        best_machine = None
        earliest_start = float('inf')

        for op in operations:
            job_id = op['job']
            machines = op['machines']
            times = op['times']
            op_idx = op['op_idx']

            # Find the earliest available time for this operation
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])

                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = op
                    best_machine = machine
                    processing_time = times[m_idx]

        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Remove the scheduled operation from the list
        operations.remove(best_op)

    return schedule
