
def heuristic(input_data):
    """FJSSP heuristic: Adaptive load balancing, SPT, EDD."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_score = float('inf')

            for machine in possible_machines:
                processing_time = possible_times[possible_machines.index(machine)]
                start_time = max(machine_available_time[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                load_factor = 1 + (machine_load[machine] / (sum(machine_load.values()) + 1e-6))
                adjusted_end_time = end_time * load_factor

                job_urgency = job_completion_times[job_id] - current_time
                score = adjusted_end_time + (0.1 * max(0, -job_urgency))

                if score < min_score:
                    min_score = score
                    best_machine = machine

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_time[best_machine], job_completion_times[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_times[job_id] = end_time
            current_time = end_time
    return schedule
