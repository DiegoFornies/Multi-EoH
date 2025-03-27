
def heuristic(input_data):
    """Schedules jobs using a shortest processing time and earliest start time heuristic."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Prioritize operations based on processing time
    operations_list = []
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            operations_list.append((job, op_idx + 1, machines, times))

    # Sort by shortest processing time
    operations_list.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations_list:
        # Find the earliest available machine and start time
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = float('inf')

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]

            start_time = max(machine_available_times[machine], job_completion_times[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = time
            elif start_time == earliest_start_time and time < processing_time:
                best_machine = machine
                processing_time = time
        
        # Update schedule
        if job not in schedule:
            schedule[job] = []

        start_time = max(machine_available_times[best_machine], job_completion_times[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
