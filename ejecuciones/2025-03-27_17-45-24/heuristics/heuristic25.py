
def heuristic(input_data):
    """
    Schedules jobs using a greedy heuristic considering machine availability and shortest processing time.
    """
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}  # When each machine is available
    job_completion_time = {job: 0 for job in jobs_data}  # When each job is completed
    
    schedule = {}
    
    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        
        for op_idx, operation in enumerate(operations):
            machines = operation[0]
            times = operation[1]
            op_num = op_idx + 1

            # Find the machine that can process the operation earliest
            best_machine, best_start_time, best_processing_time = None, float('inf'), None
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            # Update machine and job completion times
            end_time = best_start_time + best_processing_time
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            
            # Append the operation to the schedule
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
    return schedule
