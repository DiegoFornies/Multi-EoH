
def heuristic(input_data):
    """Schedules jobs based on machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1
            best_machine = None
            min_start_time = float('inf')
            processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    processing_time = times[m_idx]

            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
