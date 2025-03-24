
def heuristic(input_data):
    """FJSSP heuristic: SPT-based, earliest finish time & machine load balancing."""
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
            min_end_time = float('inf')

            # Find the best machine based on earliest finish time and machine load
            available_machines_load = [(machine, machine_load[machine]) for machine in machines]
            available_machines_load.sort(key=lambda x: x[1])

            for machine, _ in available_machines_load:
                machine_idx = machines.index(machine)
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time


            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time

    return schedule
