
def heuristic(input_data):
    """
    A heuristic for FJSSP that considers machine availability and processing time 
    to minimize makespan and balance machine load using shortest processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Sort jobs based on total processing time (shortest first)
    job_processing_times = {}
    for job, operations in jobs.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time

    sorted_jobs = sorted(jobs.keys(), key=lambda job: job_processing_times[job])

    for job in sorted_jobs:
        schedule[job] = []
        job_time = 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            
            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None #add best processing time
            
            for i, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = m
                    best_processing_time = times[i]

            # Assign the operation to the best machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability time and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time # update current job completion time
           
    return schedule
