
def heuristic(input_data):
    """Hybrid heuristic: SPT with lookahead for machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Prioritize operations based on Shortest Processing Time (SPT)
        eligible_operations.sort(key=lambda x: min(x[3]))

        job, op_num, machines, times = eligible_operations[0]

        # Lookahead: Choose machine that minimizes completion time of *next* operation
        best_machine = None
        min_next_op_completion = float('inf')
        for machine in machines:
            machine_idx = machines.index(machine)
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            completion_time = start_time + processing_time

            # Estimate completion of *next* operation on this job
            next_op_completion = completion_time #Default if it is last operation
            if op_num < len(jobs_data[job]):
                next_machines, next_times = jobs_data[job][op_num]
                if machine in next_machines:
                    next_machine_idx = next_machines.index(machine)
                    next_op_completion = completion_time + next_times[next_machine_idx] # processing time of next operation

            if next_op_completion < min_next_op_completion:
                min_next_op_completion = next_op_completion
                best_machine = machine

        machine_idx = machines.index(best_machine)
        processing_time = times[machine_idx]
        start_time = max(machine_available_time[best_machine], job_completion_time[job])

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = start_time + processing_time
        job_completion_time[job] = start_time + processing_time

        remaining_operations[job].pop(0)

    return schedule
