
def heuristic(input_data):
    """
    A heuristic for the FJSSP minimizing makespan and balancing machine load.

    It iterates through each job and its operations, selecting the machine with the earliest
    available time that minimizes idle time for both the machine and the job.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Completion time of each job

    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            op_num = op_idx + 1
            machines, times = operation

            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
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

    return schedule
