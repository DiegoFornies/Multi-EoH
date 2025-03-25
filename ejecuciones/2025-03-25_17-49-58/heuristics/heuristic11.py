
def heuristic(input_data):
    """A heuristic for FJSSP scheduling that minimizes makespan and idle time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine available times
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    
    #Prioritize jobs with longest remaining processing time
    job_priority = {}
    for job in jobs:
      job_priority[job] = sum(min(times) for machines, times in jobs[job])
    
    job_order = sorted(job_priority.items(), key=lambda item: item[1], reverse=True)

    for job_num, _ in job_order:
        job = jobs[job_num]
        schedule[job_num] = []
        current_time = 0

        for op_idx, operation in enumerate(job):
            machines, times = operation
            op_num = op_idx + 1

            # Find the earliest available machine for this operation
            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_num])
                end_time = start_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            # Assign the operation to the best machine
            schedule[job_num].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

            # Update machine available time and job completion time
            machine_available_time[best_machine] = min_end_time
            job_completion_time[job_num] = min_end_time

    return schedule
