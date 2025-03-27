
def heuristic(input_data):
    """Schedules jobs, balancing makespan, idle time, and machine load using a dynamic priority rule."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    job_priority = list(jobs.keys())

    for job in job_priority:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            best_machine, best_start_time, best_processing_time = None, float('inf'), None
            available_machines = []

            # Find feasible machines and their start times.
            for m_idx, m in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[m], job_completion_time)
                available_machines.append((m, start_time, processing_time))
            
            if not available_machines:
                raise ValueError("No feasible machine available for operation {op_num} in job {job}")

            # Prioritize machine based on weighted cost: (idle time + processing time) * (1 + machine load factor)
            best_machine, best_start_time, best_processing_time = min(
                available_machines,
                key=lambda x: (x[1] - job_completion_time + x[2]) * (1 + machine_load[x[0]]/ sum(machine_load.values()) if sum(machine_load.values())>0 else 1 )
            )

            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time = end_time

    return schedule
