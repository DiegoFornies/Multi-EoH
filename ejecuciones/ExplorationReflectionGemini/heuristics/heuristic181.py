
def heuristic(input_data):
    """FJSSP heuristic: SPT+Load Balance, dynamic weights."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for op_index, op_data in enumerate(jobs[job_id]):
            machines, times = op_data
            best_machine, best_start_time, best_processing_time = None, 0, 0
            min_metric = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_load[machine], job_completion_times[job_id])
                end_time = start_time + processing_time
                metric = end_time + 0.01 * machine_load[machine] + 0.001 * processing_time

                if metric < min_metric:
                    min_metric = metric
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

    return schedule
