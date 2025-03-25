
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing idle time on machines
    and job completion times by selecting the machine with the earliest available time
    for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}  # Store the resulting schedule
    machine_available_time = {m: 0 for m in range(n_machines)}  # Track when each machine is available
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Track when each job is completed
    
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        
        for operation_index, operation_data in enumerate(jobs_data[job]):
            machines, times = operation_data
            
            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_end_time = float('inf')
            
            for machine_index, machine in enumerate(machines):
                processing_time = times[machine_index]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
            
            # Schedule the operation on the selected machine
            operation_number = operation_index + 1
            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            
            # Update machine available time and job completion time
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time
            
    return schedule
