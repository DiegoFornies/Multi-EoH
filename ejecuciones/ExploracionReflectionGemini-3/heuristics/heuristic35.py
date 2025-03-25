
def heuristic(input_data):
    """Schedules jobs based on shortest processing time and earliest available machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    #Prioritize jobs based on total processing time
    job_priorities = {}
    for job, operations in jobs.items():
        total_processing_time = sum(min(times) for machines, times in operations)
        job_priorities[job] = total_processing_time
    
    sorted_jobs = sorted(job_priorities.keys(), key=lambda job: job_priorities[job])

    for job in sorted_jobs:
        operations = jobs[job]
        current_time = 0
        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            start_time = max(machine_available_time[best_machine], job_completion_time[job])

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = start_time + best_processing_time
            job_completion_time[job] = start_time + best_processing_time

    return schedule
