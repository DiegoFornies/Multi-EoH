
def heuristic(input_data):
    """Heuristic for FJSSP: Minimizes makespan with job completion time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(n_jobs)}

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            # Choose machine that minimizes the job's completion time
            best_machine = None
            min_completion_time = float('inf')

            for machine_id in possible_machines:
                processing_time = possible_times[possible_machines.index(machine_id)]
                start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine_id

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            current_time = end_time

    return schedule
