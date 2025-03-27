
def heuristic(input_data):
    """Schedules jobs using a shortest processing time and earliest start time heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_num in jobs:
        schedule[job_num] = []
        operations = jobs[job_num]
        
        for op_idx, op_data in enumerate(operations):
            eligible_machines = op_data[0]
            processing_times = op_data[1]
            
            best_machine = None
            min_end_time = float('inf')
            
            # Iterate through available machines for the operation
            for i, machine in enumerate(eligible_machines):
                processing_time = processing_times[i]
                
                # Earliest possible start time is the maximum of machine availability and job completion
                start_time = max(machine_available_time[machine], job_completion_time[job_num])
                end_time = start_time + processing_time
                
                # Select the machine that minimizes the end time
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
            
            # Assign the operation to the best machine
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_num] = best_start_time + best_processing_time
            
            schedule[job_num].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
