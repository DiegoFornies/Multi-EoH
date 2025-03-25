
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes machines with the earliest available time.
    It considers both machine availability and job dependencies to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs_data:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation

            # Find the machine with the earliest available time among feasible machines
            best_machine, best_time, earliest_start = None, float('inf'), float('inf')
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    best_time = times[m_idx]

            # Assign the operation to the selected machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
