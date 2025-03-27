
def heuristic(input_data):
    """A heuristic to solve the FJSSP by prioritizing shorter operations and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)} # Keep track of how busy each machine is
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)} # Keep track of when each job is completed

    # Prioritize operations based on shortest processing time first.
    # Key Improvement: Create a list of all operations and sort them.
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))
    
    # Sort operations by their shortest possible processing time
    operations.sort(key=lambda op: min(op[3]))

    for job, op_num, machines, times in operations:
        
        best_machine = None
        min_end_time = float('inf')
        processing_time = 0
        # Key Improvement: Consider all possible machines and select one that minimize makespan
        for m_idx, machine in enumerate(machines):
            proc_time = times[m_idx]

            start_time = max(machine_load[machine], job_completion_times[job])
            end_time = start_time + proc_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = proc_time
        
        start_time = max(machine_load[best_machine], job_completion_times[job])
        end_time = start_time + processing_time
        
        if job not in schedule:
          schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[best_machine] = end_time # Update the load of the selected machine
        job_completion_times[job] = end_time # Update job completion time
    
    return schedule
