
def heuristic(input_data):
    """Combines minimizing idle time and Earliest Due Date (EDD) for scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs by job number to mimic EDD.
    job_order = sorted(jobs_data.keys())

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Find the machine that minimizes idle time.
            best_machine = None
            min_idle = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                idle_time = max(0, machine_available_time[machine] - current_time)

                if idle_time < min_idle:
                    min_idle = idle_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine.
            if best_machine is None:
                best_machine = machines[0]
                best_processing_time = times[0]

            start_time = max(machine_available_time[best_machine], current_time)
            processing_time = best_processing_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine available time and job completion time.
            machine_available_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
