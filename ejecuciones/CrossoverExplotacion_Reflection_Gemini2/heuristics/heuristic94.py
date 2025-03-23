
def heuristic(input_data):
    """Combines SPT, earliest start, and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id, job_ops in jobs.items():
        schedule[job_id] = []
        op_start_time = 0  # Correctly initialize op_start_time here
        for op_idx, (machines, times) in enumerate(job_ops):
            op_num = op_idx + 1
            best_machine = None
            min_end_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_load[machine], op_start_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_load[best_machine], op_start_time)
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = end_time
            job_completion[job_id] = end_time
            op_start_time = end_time # Update start time for next operation
    return schedule
