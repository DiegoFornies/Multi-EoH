
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that prioritizes
    machines with the earliest available time to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(1, n_machines + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    remaining_operations = {}
    for job, operations in jobs.items():
        remaining_operations[job] = [(i + 1, op) for i, op in enumerate(operations)]

    completed_operations = {job: 0 for job in range(1, n_jobs + 1)}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num, (machines, times) = operations[0]
                eligible_operations.append((job, op_num, machines, times))

        if not eligible_operations:
            break  # No more operations to schedule

        best_operation = None
        earliest_start_time = float('inf')

        for job, op_num, machines, times in eligible_operations:
            best_machine = None
            best_time = float('inf')

            for i, m in enumerate(machines):
                available_time = machine_available_time[m]
                start_time = max(available_time, job_completion_time[job])

                if start_time < best_time:
                    best_time = start_time
                    best_machine = m

            if best_time < earliest_start_time:
                earliest_start_time = best_time
                best_operation = (job, op_num, best_machine, machines, times)

        if best_operation:
            job, op_num, assigned_machine, machines, times = best_operation
            machine_index = machines.index(assigned_machine)
            processing_time = times[machine_index]

            start_time = max(machine_available_time[assigned_machine], job_completion_time[job])
            end_time = start_time + processing_time
            machine_available_time[assigned_machine] = end_time
            job_completion_time[job] = end_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            remaining_operations[job].pop(0)
    return schedule
