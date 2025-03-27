
def heuristic(input_data):
    """Hybrid heuristic: SPT + least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0 

        for op_index, operation in enumerate(jobs[job_id]):
            eligible_machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_time_load = float('inf')

            for machine_index, machine_id in enumerate(eligible_machines):
                time = processing_times[machine_index]
                # Consider both processing time and machine load
                time_load = time + machine_load[machine_id]  

                if time_load < min_time_load:
                    min_time_load = time_load
                    best_machine = machine_id
                    best_processing_time = time

            start_time = max(current_time, machine_load[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = end_time
            job_completion_time[job_id] = end_time
            current_time = end_time

    return schedule
