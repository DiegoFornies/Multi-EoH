
def heuristic(input_data):
    """Greedy heuristic: Assigns operations to earliest available machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for operation_index, operation_data in enumerate(jobs[job_id]):
            machines = operation_data[0]
            times = operation_data[1]

            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job_id])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[i]
                    best_start_time = start_time

            machine_time[best_machine] = min_end_time
            job_completion_time[job_id] = min_end_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': processing_time
            })

    return schedule
