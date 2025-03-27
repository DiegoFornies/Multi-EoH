
def heuristic(input_data):
    """Aims to minimize makespan by scheduling operations based on earliest start time,
    considering both machine availability and job completion time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Use job numbers directly

    for job in range(1, n_jobs + 1):  # Iterate through job numbers
        schedule[job] = []
        job_ops = jobs_data[job]
        
        for op_idx, (machines, times) in enumerate(job_ops):
            operation_number = op_idx + 1

            # Find the machine with the earliest available time that can perform the operation
            best_machine = None
            earliest_start_time = float('inf')
            processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    processing_time = times[m_idx]

            # Schedule the operation on the selected machine
            start_time = earliest_start_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine available time and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
