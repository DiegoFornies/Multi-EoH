
def heuristic(input_data):
    """
    Schedules jobs based on shortest processing time first (SPT) and earliest available machine.
    Prioritizes jobs with shorter total processing times and selects the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Calculate total processing time for each job
    job_processing_times = {}
    for job, operations in jobs.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time

    # Sort jobs based on total processing time (shortest first)
    sorted_jobs = sorted(jobs.keys(), key=lambda job: job_processing_times[job])

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs.keys()}

    for job in sorted_jobs:
        schedule[job] = []
        operations = jobs[job]
        for op_idx, (machines, times) in enumerate(operations):
            op_num = op_idx + 1
            
            # Find the machine that can start the operation earliest
            best_machine = None
            earliest_start_time = float('inf')

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_time = times[m_idx]
            
            # Schedule the operation on the selected machine
            start_time = earliest_start_time
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine and job completion times
            machine_available_times[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
