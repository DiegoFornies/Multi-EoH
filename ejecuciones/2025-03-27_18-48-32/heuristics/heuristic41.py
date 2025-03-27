
def heuristic(input_data):
    """Combines machine load balancing and idle time minimization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_times = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_end_time = float('inf')

            # Find machine that minimizes end time
            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine_id], current_time)
                end_time = start_time + processing_time
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id

            # Tie-breaker: balance machine load
            contenders = [m for m in possible_machines if max(machine_available_times[m], current_time) + possible_times[possible_machines.index(m)] == min_end_time]
            if len(contenders) > 1:
                best_machine = min(contenders, key=lambda m: machine_load[m])

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_times[best_machine], current_time)
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
            current_time = end_time

    return schedule
