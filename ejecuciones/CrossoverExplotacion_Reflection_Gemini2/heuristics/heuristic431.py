
def heuristic(input_data):
    """Combines earliest start time with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        earliest_start_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            min_start_time = float('inf')
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available[machine_id]
                start_time = max(available_time, job_completion[job_id])
                min_start_time = min(min_start_time, start_time)

            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_job, best_op_index = job_id, op_index

        job_id, op_index = best_job, best_op_index
        machines, times = jobs_data[job_id][op_index]

        best_machine = None
        min_end_time = float('inf')
        min_workload = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available[machine], job_completion[job_id])
            end_time = start_time + processing_time
            workload = machine_workload[machine]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                min_workload = workload
            elif end_time == min_end_time:
                if workload < min_workload:
                    best_machine = machine
                    best_processing_time = processing_time
                    min_workload = workload

        start_time = max(machine_available[best_machine], job_completion[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available[best_machine] = end_time
        job_completion[job_id] = end_time
        machine_workload[best_machine] += best_processing_time

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
