
def heuristic(input_data):
    """Schedules jobs using a SPT-inspired heuristic with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            best_machine = None
            min_weighted_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                # Weight processing time by current machine load
                weighted_time = processing_time * (1 + machine_load[machine])
                start_time = max(machine_load[machine], job_completion[job_id])

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            machine_load[best_machine] = best_start_time + best_processing_time
            job_completion[job_id] = best_start_time + best_processing_time
            
    return schedule
