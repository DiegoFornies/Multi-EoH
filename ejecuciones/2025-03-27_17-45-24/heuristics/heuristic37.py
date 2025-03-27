
def heuristic(input_data):
    """Prioritizes shortest processing time and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            operation_number = op_idx + 1

            # Find machine with shortest processing time, considering machine load.
            best_machine = None
            min_end_time = float('inf')
            selected_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    selected_time = times[m_idx]

            # Schedule operation.
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + selected_time
            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': selected_time
            })

            # Update machine load and job completion time.
            machine_load[best_machine] += selected_time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
