
def heuristic(input_data):
    """Combines SPT and least loaded machine for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    delay_factor = 0.05  # Adjust for load balancing

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    for operation in operations:
        job_id = operation['job']
        op_num = operation['operation']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_completion_time = float('inf')
        processing_time = 0

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_last_end_time[job_id])
            completion_time = start_time + times[i] + machine_load[machine] * delay_factor

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                processing_time = times[i]

        start_time = max(machine_available_time[best_machine], job_last_end_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_last_end_time[job_id] = end_time
        machine_load[best_machine] += processing_time

    return schedule
