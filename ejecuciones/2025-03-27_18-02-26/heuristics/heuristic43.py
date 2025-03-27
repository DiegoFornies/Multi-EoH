
def heuristic(input_data):
    """Aims to minimize makespan by scheduling operations greedily."""
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    machine_times = {m: 0 for m in range(n_machines)}
    job_finish_times = {job: 0 for job in jobs_data}
    schedule = {}

    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        for op_idx, op_data in enumerate(operations):
            machines, processing_times = op_data
            op_num = op_idx + 1

            # Select machine with earliest available time
            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_times[machine], job_finish_times[job_id])
                end_time = start_time + processing_times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_times[m_idx]
                    best_start_time = start_time

            machine_times[best_machine] = min_end_time
            job_finish_times[job_id] = min_end_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })
    return schedule
