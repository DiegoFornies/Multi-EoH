
def heuristic(input_data):
    """Combines SPT, earliest completion, & machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Sort jobs by total processing time (Shortest Processing Time first)
    job_priority = sorted(jobs.keys(), key=lambda job_id: sum(min(times) for _, times in jobs[job_id]))

    for job in job_priority:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine = -1
            best_start_time = float('inf')
            best_processing_time = -1
            min_completion_time = float('inf')

            # Find the best machine based on earliest completion time and load
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time or (completion_time == min_completion_time and machine_load[machine] < sum(machine_load.values()) / len(machine_load)):
                    min_completion_time = completion_time
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = best_start_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            machine_load[best_machine] += best_processing_time

    return schedule
