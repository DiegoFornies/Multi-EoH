
def heuristic(input_data):
    """Hybrid heuristic: SPT for makespan, machine load balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_num, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        machine_loads = {m: 0 for m in machines}
        for m in machines:
            machine_loads[m] = machine_available_time[m]
        
        # Find the best machine, prioritize less loaded machines
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]
            if end_time < min_end_time:
              min_end_time = end_time
              best_machine = machine
              processing_time = times[i]
            elif end_time == min_end_time and machine_loads[machine] < machine_loads[best_machine if best_machine else machine]:
              best_machine = machine
              processing_time = times[i]

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
