
def heuristic(input_data):
    """Schedules jobs, minimizing idle time and balancing load.
    Uses a greedy approach with machine load consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0
        for op_idx, (machines, times) in enumerate(jobs[job_id]):
            op_num = op_idx + 1
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(current_time, machine_available_time[machine_id])
                # Consider machine load in tie-breaking.
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine_id
                    best_processing_time = processing_time
                elif start_time == min_start_time and machine_load[machine_id] < machine_load.get(best_machine, float('inf')):
                    best_machine = machine_id
                    best_processing_time = processing_time
            start_time = max(current_time, machine_available_time[best_machine])
            end_time = start_time + best_processing_time
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            current_time = end_time

    return schedule
