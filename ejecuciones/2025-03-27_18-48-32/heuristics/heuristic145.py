
def heuristic(input_data):
    """Combines earliest start time and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]
            best_machine = None
            min_score = float('inf')

            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, current_time)
                end_time = start_time + processing_time
                # Combine makespan and load:
                score = end_time + machine_load[machine_id] * 0.1 

                if score < min_score:
                    min_score = score
                    best_machine = machine_id

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
