
def heuristic(input_data):
    """
    Heuristic for FJSSP minimizing makespan, idle time, and balancing machine load.
    Schedules operations based on shortest processing time and earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs_data[job_id]

        for op_idx, operation in enumerate(job_operations):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_end_time = float('inf')

            for machine_idx, machine in enumerate(possible_machines):
                processing_time = possible_times[machine_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = min_end_time
            job_completion_times[job_id] = min_end_time

    return schedule
