
def heuristic(input_data):
    """A heuristic for the Flexible Job Shop Scheduling Problem."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}

    # Sort jobs based on total processing time
    job_processing_times = {}
    for job, operations in jobs.items():
        total_time = sum(min(times) for machines, times in operations)  # Use the minimum processing time
        job_processing_times[job] = total_time

    sorted_jobs = sorted(job_processing_times.keys(), key=lambda job: job_processing_times[job])

    for job in sorted_jobs:
        operations = jobs[job]
        for op_idx, (machines, times) in enumerate(operations):
            op_num = op_idx + 1
            best_machine, best_start_time, best_processing_time = None, float('inf'), None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = best_start_time
            end_time = start_time + best_processing_time
            machine = best_machine

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[machine] = end_time
            job_completion_times[job] = end_time
    
    return schedule
