
def heuristic(input_data):
    """FJSSP heuristic: Combines EDD, SPT and adaptive load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_due_time = {}
    for job in range(1, n_jobs + 1):
        job_due_time[job] = sum(min(times) for machines, times in jobs_data[job]) * 1.5

    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times, job_due_time[job]))

        # Sort by EDD primarily, then machine availability.
        eligible_operations.sort(key=lambda x: (x[4], machine_available_time[min(x[2], key=lambda m:machine_available_time[m])]))

        job, op_num, machines, times, _ = eligible_operations[0]

        # Adaptive machine selection
        best_machine = None
        min_end_time = float('inf')
        total_load = sum(machine_available_time.values())
        
        for machine in machines:
            processing_time = times[machines.index(machine)]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            load_factor = 1 + (machine_available_time[machine] / total_load if total_load > 0 else 0)
            adjusted_end_time = end_time * load_factor # Penalizing highly loaded machines

            if adjusted_end_time < min_end_time:
                min_end_time = adjusted_end_time
                best_machine = machine

        processing_time = times[machines.index(best_machine)]
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        remaining_operations[job].pop(0)

    return schedule
