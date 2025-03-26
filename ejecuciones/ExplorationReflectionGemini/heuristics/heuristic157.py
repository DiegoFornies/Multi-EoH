
def heuristic(input_data):
    """Prioritizes shortest processing time and machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start = start_time
                    best_time = processing_time

            machine_available[best_machine] = best_start + best_time
            job_completion[job_id] = best_start + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start,
                'End Time': best_start + best_time,
                'Processing Time': best_time
            })

    return schedule
