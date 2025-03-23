
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing workload, Combines elements from two parents."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        earliest_finish_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            min_finish_time = float('inf')
            selected_machine = None
            processing_time = None

            for machine_id, time in zip(machines, times):
                start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
                finish_time = start_time + time
                weighted_finish = 0.7 * finish_time + 0.3 * machine_load[machine_id]
                
                if weighted_finish < min_finish_time:
                   min_finish_time = weighted_finish
                   selected_machine = machine_id
                   processing_time = time

            if min_finish_time < earliest_finish_time:
                earliest_finish_time = min_finish_time
                best_job = job_id
                best_op_index = op_index

        job_id, op_index = best_job, best_op_index
        machines, times = jobs_data[job_id][op_index]

        # Find the selected machine from the inner loop.
        min_finish_time = float('inf')
        best_machine, best_processing_time = None, None

        for machine_id, time in zip(machines, times):
                start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
                finish_time = start_time + time
                weighted_finish = 0.7 * finish_time + 0.3 * machine_load[machine_id]

                if weighted_finish <= min_finish_time:
                    min_finish_time = weighted_finish
                    best_machine = machine_id
                    best_processing_time = time


        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[best_machine] += best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
