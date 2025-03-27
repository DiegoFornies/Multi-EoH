
def heuristic(input_data):
    """FJSSP heuristic: SPT with adaptive machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            # Choose machine: SPT + Adaptive Load balancing
            best_machine = None
            min_end_time = float('inf')

            for machine in possible_machines:
                processing_time = possible_times[possible_machines.index(machine)]
                start_time = max(machine_available_time[machine], current_time)
                end_time = start_time + processing_time

                # Adaptive load balancing: dynamically adjust the influence of load
                load_factor = 1 + (machine_load[machine] / sum(machine_load.values()) if sum(machine_load.values()) > 0 else 0) 
                adjusted_end_time = end_time * load_factor  # Penalize more loaded machines
                
                if adjusted_end_time < min_end_time:
                    min_end_time = adjusted_end_time
                    best_machine = machine

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_time[best_machine], current_time)
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
            current_time = end_time
            job_completion_time[job_id] = end_time

    return schedule
