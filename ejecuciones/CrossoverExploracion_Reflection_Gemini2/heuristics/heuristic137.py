
def heuristic(input_data):
    """Schedules jobs using a greedy approach minimizing makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    job_next_operation = {j: 0 for j in jobs_data}

    while True:
        eligible_operations = []
        for job_id in jobs_data:
            next_op_index = job_next_operation[job_id]
            if next_op_index < len(jobs_data[job_id]):
                eligible_operations.append((job_id, next_op_index))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]
            for i, machine in enumerate(machines):
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    processing_time = time

        job_id, op_index = best_operation
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        job_next_operation[job_id] += 1

    return schedule
