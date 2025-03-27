
def heuristic(input_data):
    """
    Heuristic scheduling algorithm for FJSSP. Chooses the machine with the earliest
    available time for each operation, minimizing makespan and balancing machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}  # Earliest available time for each machine
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Completion time of each job

    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_end_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the chosen machine
            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
