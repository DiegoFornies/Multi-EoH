
def heuristic(input_data):
    """Prioritizes jobs based on total processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    job_processing_times = {}
    for job, operations in jobs.items():
        total_time = sum(min(times) for _, times in operations)
        job_processing_times[job] = total_time

    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1], reverse=True)

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job, _ in sorted_jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': min_start_time,
                'End Time': min_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = min_start_time + best_processing_time
            job_completion_time[job] = min_start_time + best_processing_time

    return schedule
