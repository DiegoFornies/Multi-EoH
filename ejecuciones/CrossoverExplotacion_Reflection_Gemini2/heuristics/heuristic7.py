
def heuristic(input_data):
    """A heuristic for FJSSP minimizing makespan by assigning operations to the earliest available machine and time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    
    for job_id in jobs:
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1
            
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None
            
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                    
            if best_machine is not None:
                start_time = min_start_time
                end_time = start_time + best_processing_time
                
                schedule[job_id].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })
                
                machine_available_times[best_machine] = end_time
                job_completion_times[job_id] = end_time
            else:
                # Handle case where no machine is available (shouldn't happen with valid input, but good to have)
                print(f"Warning: No suitable machine found for job {job_id}, operation {op_num}. Skipping.")
                continue # or raise an exception, depending on desired behavior
    
    return schedule
