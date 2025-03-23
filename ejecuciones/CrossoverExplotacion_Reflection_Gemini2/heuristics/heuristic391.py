
def heuristic(input_data):
    """Combines earliest finish time, SPT, and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs_data[job_id]):
            machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_end_time = float('inf')
            min_processing_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time
                load_factor = machine_load[machine] / (sum(machine_load.values()) + 1e-6) if sum(machine_load.values())>0 else 0
                
                weighted_end_time = 0.7*end_time + 0.3*(load_factor*10)

                if weighted_end_time < min_end_time:
                    min_end_time = weighted_end_time
                    best_machine = machine
                    best_processing_time = processing_time

                elif weighted_end_time == min_end_time and processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            machine_load[best_machine] += best_processing_time

    return schedule
