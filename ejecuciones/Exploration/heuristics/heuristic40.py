
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that considers minimizing idle time
    and balancing machine load by prioritizing operations with shorter processing times
    and selecting the machine with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times

    for job_id in jobs:
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation

            # Find the best machine for the operation
            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_time = processing_time
                    best_start = start_time

            # Schedule the operation on the best machine
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start,
                'End Time': min_end_time,
                'Processing Time': best_time
            })

            # Update machine available time and job completion time
            machine_available_time[best_machine] = min_end_time
            job_completion_time[job_id] = min_end_time

    return schedule
