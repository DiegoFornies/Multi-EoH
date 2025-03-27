
def heuristic(input_data):
    """Combines shortest job and least loaded machine, prioritizing job completion."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(current_time, machine_time[machine])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            start_time = min_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            current_time = end_time
            job_completion_time[job_id] = end_time

    return schedule
