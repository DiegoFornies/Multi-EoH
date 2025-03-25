
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing idle time
    on machines and balancing workload by choosing the machine
    with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            end_time = best_start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
