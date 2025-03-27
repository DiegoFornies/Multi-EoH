
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritize shortest processing time and least loaded machine."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Flatten operations for sorting and processing
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))  # Job ID, op number, machines, times

    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op[3]))  # sort by min processing time

    for job_id, op_num, machines, times in operations:
        # Find the best machine based on shortest processing time and least load
        best_machine, min_end_time = None, float('inf')

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_load[machine], job_completion_times[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine

        # Schedule the operation
        start_time = max(machine_load[best_machine], job_completion_times[job_id])
        processing_time = times[machines.index(best_machine)]
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

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
