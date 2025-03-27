
def heuristic(input_data):
    """Schedules jobs prioritizing machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, op_data in enumerate(jobs[job_id]):
            machines, times = op_data
            op_num = op_idx + 1

            best_machine = None
            min_load = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                load = machine_load[machine]
                if load < min_load:
                    min_load = load
                    best_machine = machine
                    best_processing_time = processing_time

            if best_machine is not None:
                start_time = max(machine_load[best_machine], job_completion_time[job_id])
                end_time = start_time + best_processing_time

                schedule[job_id].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_time[job_id] = end_time
            else:
                print(f"No machine found for job {job_id}, operation {op_num}")
                return None

    return schedule
