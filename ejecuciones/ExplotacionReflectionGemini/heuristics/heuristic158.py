
def heuristic(input_data):
    """Combines job priority and minimizing machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    job_priority = {}
    for job_id in range(1, n_jobs + 1):
        job_priority[job_id] = len(jobs_data[job_id])

    sorted_jobs = sorted(job_priority.items(), key=lambda item: item[1])

    for job_id, _ in sorted_jobs:
        schedule[job_id] = []
        job_operations = jobs_data[job_id]

        for op_idx, operation in enumerate(job_operations):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_idle_time = float('inf')
            earliest_start = float('inf')
            selected_processing_time = None
            selected_start_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                idle_time = start_time - machine_available_time[machine] if start_time > machine_available_time[machine] else 0
                
                if idle_time < min_idle_time:
                    min_idle_time = idle_time
                    best_machine = machine
                    earliest_start = start_time
                    selected_processing_time = processing_time
                    
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': earliest_start,
                'End Time': earliest_start + selected_processing_time,
                'Processing Time': selected_processing_time
            })

            machine_available_time[best_machine] = earliest_start + selected_processing_time
            job_last_end_time[job_id] = earliest_start + selected_processing_time
            machine_load[best_machine] += selected_processing_time

    return schedule
