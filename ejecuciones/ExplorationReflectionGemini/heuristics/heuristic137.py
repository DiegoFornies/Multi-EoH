
def heuristic(input_data):
    """Aims to minimize makespan by prioritizing operations on least loaded machines."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    for job_id in jobs:
        for op_idx, operation_data in enumerate(jobs[job_id]):
            machines, times = operation_data
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

    return schedule
