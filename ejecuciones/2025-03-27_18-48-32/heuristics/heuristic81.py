
def heuristic(input_data):
    """Combines load balancing and job completion to minimize makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            # Choose machine with the lowest current load AND earliest available time
            best_machine = min(possible_machines, key=lambda m: (machine_load[m], machine_available_times[m]))

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_times[best_machine], job_completion_time[job_id], current_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time[job_id] = end_time
            current_time = end_time

    return schedule
