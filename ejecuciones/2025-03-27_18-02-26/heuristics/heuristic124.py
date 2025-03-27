
def heuristic(input_data):
    """Combines SPT, machine load, and job completion time for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            best_machine = None
            min_time_load = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                available_start_time = max(machine_available_time[machine], job_completion_time[job_id])
                time_load = processing_time + available_start_time #Consider available start time.

                if time_load < min_time_load:
                    min_time_load = time_load
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(current_time, machine_available_time[best_machine], job_completion_time[job_id]) # ensure sequence and machine constraints
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            current_time = end_time

    return schedule
