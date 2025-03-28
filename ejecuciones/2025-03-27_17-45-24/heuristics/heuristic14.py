
def heuristic(input_data):
    """A heuristic for FJSSP that aims to minimize makespan and balance machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Completion time of each job
    machine_assignments = {m: [] for m in range(n_machines)}  # Keep track of machine assignments

    for job_id, operations in jobs.items():
        schedule[job_id] = []

        for op_idx, operation in enumerate(operations):
            machines = operation[0]
            times = operation[1]
            op_num = op_idx + 1
            
            # Find the earliest available machine for the operation, considering job completion time
            best_machine = None
            min_start_time = float('inf')
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time  # Capture the selected machine's processing time
            
            # Schedule the operation on the best machine
            start_time = min_start_time
            end_time = start_time + best_processing_time
            
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
            # Update machine and job completion times
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            machine_assignments[best_machine].append((job_id, op_num))
    
    return schedule
