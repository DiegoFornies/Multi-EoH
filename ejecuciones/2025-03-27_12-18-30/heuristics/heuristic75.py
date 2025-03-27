
def heuristic(input_data):
    """Hybrid heuristic: SPT for makespan, load balancing to separate."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, op_data in enumerate(jobs[job_id]):
            machines, times = op_data
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')
            min_load = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                load = machine_available_time[machine]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    min_load = load
                elif end_time == min_end_time and load < min_load:
                    best_machine = machine
                    best_processing_time = processing_time
                    min_load = load

            if best_machine is not None:
                start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
                end_time = start_time + best_processing_time
                schedule[job_id].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_available_time[best_machine] = end_time
                job_completion_time[job_id] = end_time
            else:
                print(f"Warning: No machine for job {job_id}, operation {op_num}")
                return None

    return schedule
