
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing idle time on machines
    and early completion of operations. It uses a greedy approach to assign
    machines and schedule operations, considering both machine availability
    and job completion time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    for job_id in jobs_data:
        schedule[job_id] = []
        for operation_index, operation_data in enumerate(jobs_data[job_id]):
            machines = operation_data[0]
            processing_times = operation_data[1]

            # Find the best machine for the operation
            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_times[i]
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_times[i]

            # Schedule the operation on the best machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time
            
            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
