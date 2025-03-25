
def heuristic(input_data):
    """A heuristic to solve FJSSP, minimizing makespan and balancing load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize data structures
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}

    # Sort jobs by number of operations (shortest job first)
    job_order = sorted(jobs.keys(), key=lambda job: len(jobs[job]))

    for job in job_order:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time that can perform the operation
            best_machine, best_time = None, float('inf')
            for i, m in enumerate(machines):
                available_time = max(machine_available_time[m], job_completion_time[job])
                if available_time < best_time:
                    best_time = available_time
                    best_machine = m
                    processing_time = times[i] #Select processing time according to best_machine

            # Schedule the operation on the selected machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine available time and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            machine_load[best_machine] += processing_time
    return schedule
