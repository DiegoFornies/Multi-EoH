
def heuristic(input_data):
    """Heuristic for FJSSP: Combines job priority and machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    job_priority = {}
    for job_id in range(1, n_jobs + 1):
        job_priority[job_id] = (len(jobs_data[job_id]))

    sorted_jobs = sorted(job_priority.items(), key=lambda item: item[1])

    for job_id, _ in sorted_jobs:
        schedule[job_id] = []
        job_operations = jobs_data[job_id]

        for op_idx, operation in enumerate(job_operations):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_idle_time = float('inf') #Prioritize minimizing machine idle time
            earliest_start_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + processing_time

                idle_time = start_time - machine_available_time[machine] if machine_available_time[machine] > 0 else start_time
                
                if idle_time < min_idle_time: #Prioritize less idle time
                    min_idle_time = idle_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
                    earliest_start_time = start_time

                elif idle_time == min_idle_time and start_time < earliest_start_time: #Tie Break 1: Earliest start time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
                    earliest_start_time = start_time
                elif idle_time == min_idle_time and start_time == earliest_start_time and machine_load[machine] < machine_load[best_machine]:  # Tie Break 2: Lower Machine Load
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
                    earliest_start_time = start_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_last_end_time[job_id] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time

    return schedule
