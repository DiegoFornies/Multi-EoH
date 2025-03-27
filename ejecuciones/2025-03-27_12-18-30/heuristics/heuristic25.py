
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes jobs based on shortest processing time first (SPT).
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Calculate total processing time for each job
    job_processing_times = {}
    for job, operations in jobs_data.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)  # Assuming we pick the shortest time on any available machine
        job_processing_times[job] = total_time

    # Sort jobs based on shortest processing time
    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1])
    scheduled_jobs = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    for job_num, _ in sorted_jobs:
        job_schedule = []
        current_time = 0

        for op_idx, operation in enumerate(jobs_data[job_num]):
            machines, times = operation

            # Find the machine with the earliest available time among the feasible machines
            best_machine = None
            earliest_start = float('inf')
            processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                start_time = max(current_time, machine_available_time[machine])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    processing_time = times[i]
            
            start_time = max(current_time, machine_available_time[best_machine])
            end_time = start_time + processing_time
            
            job_schedule.append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine availability and current job time
            machine_available_time[best_machine] = end_time
            current_time = end_time

        scheduled_jobs[job_num] = job_schedule

    return scheduled_jobs
