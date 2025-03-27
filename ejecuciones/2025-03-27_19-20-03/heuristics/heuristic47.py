
def heuristic(input_data):
    """Heuristic for FJSSP: Earliest Due Date with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_due_dates = {}  
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Calculate job due dates based on total processing time.
    for job, operations in jobs_data.items():
        total_processing_time = 0
        for machines, times in operations:
            total_processing_time += min(times)  # Approximate total time
        job_due_dates[job] = total_processing_time

    operation_queue = []
    for job, operations in jobs_data.items():
        operation_queue.append((job, 0))

    scheduled_operations = set()

    while operation_queue:
        # Prioritize jobs with earlier due dates.
        operation_queue.sort(key=lambda x: job_due_dates[x[0]])

        best_operation = None
        best_machine = None
        min_start_time = float('inf')

        for job_id, op_index in operation_queue:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = processing_time

        job_id, op_index = best_operation
        machines, times = jobs_data[job_id][op_index]

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        scheduled_operations.add((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            operation_queue.append((job_id, op_index + 1))

        operation_queue.remove(best_operation)

    return schedule
