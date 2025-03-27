
def heuristic(input_data):
    """Schedules jobs by assigning each operation to the machine that results in the earliest possible completion time, minimizing makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        current_time = 0
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine = None
            earliest_end_time = float('inf')
            best_start_time = None
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], current_time)
                end_time = start_time + processing_time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': earliest_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = earliest_end_time
            current_time = earliest_end_time
            job_completion_time[job] = earliest_end_time

    return schedule
