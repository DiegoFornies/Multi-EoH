
def heuristic(input_data):
    """Heuristic for FJSSP: Chooses machine with earliest available time, minimizes idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        ops = jobs[job]
        current_time = 0 #start the first job at 0

        for op_idx, operation in enumerate(ops):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine that allows the earliest start time
            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job]) #Mathcing both machine and job
               
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine
            start_time = earliest_start_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
