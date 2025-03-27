
def heuristic(input_data):
    """Schedules jobs using Shortest Processing Time (SPT) for operations."""
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
                eligible_operations.append((job, op_num, machines, times, job))

        # Shortest Processing Time First
        best_operation = None
        min_processing_time = float('inf')

        for job, op_num, machines, times, job_id in eligible_operations:
            for m_idx, m in enumerate(machines):
                processing_time = times[m_idx]
                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_operation = (job, op_num, m, processing_time, job_id)

        if best_operation:
            job, op_num, machine, processing_time, job_id = best_operation
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = start_time + processing_time
            job_completion_time[job_id] = start_time + processing_time
            remaining_operations[job_id].pop(0)

    return schedule
