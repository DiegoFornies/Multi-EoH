
def heuristic(input_data):
    """Schedules jobs by earliest start time and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs_data:
        schedule[job] = []
        current_time = 0
        for op_num, operation in enumerate(jobs_data[job]):
            machines, times = operation
            best_machine = None
            min_start = float('inf')
            processing_time = 0

            for i, machine in enumerate(machines):
                start_time = max(machine_load[machine], current_time)
                if start_time < min_start:
                    min_start = start_time
                    best_machine = machine
                    processing_time = times[i]

            start_time = min_start
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_load[best_machine] = end_time
            current_time = end_time
            job_completion[job] = end_time
    return schedule
