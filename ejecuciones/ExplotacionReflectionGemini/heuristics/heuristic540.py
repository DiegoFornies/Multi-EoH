
def heuristic(input_data):
    """Heuristic for FJSSP: SPT with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine load

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    while available_operations:
        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]
            
            # SPT - Shortest Processing Time
            min_proc_time = float('inf')
            best_local_machine = None
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                
                if processing_time < min_proc_time:
                    min_proc_time = processing_time
                    best_local_machine = (machine, processing_time, start_time, end_time)
                
            
            # Load balancing consideration: Choose the machine that has the least current load
            machine, processing_time, start_time, end_time = best_local_machine
            
            #Adjust for machine load: adding machine_load penalty
            adjusted_start_time = max(machine_available_time[machine], job_completion_time[job_id]) + machine_load[machine]*0.001 # adding penalty
            adjusted_end_time = adjusted_start_time + processing_time
           
            
            if adjusted_end_time < min_end_time:
                    min_end_time = adjusted_end_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[machine] += processing_time # Update machine_load
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    return schedule
