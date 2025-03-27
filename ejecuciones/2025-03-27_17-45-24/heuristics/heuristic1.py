
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes machine load balancing and minimizing job idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine load
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)} # Keep track of the job completion time

    # Calculate total processing time for each job to estimate job priority.
    job_processing_times = {}
    for job_id, operations in jobs.items():
        total_time = sum(min(op[1]) for op in operations)
        job_processing_times[job_id] = total_time
    
    # Sort jobs by total processing time (shortest first) to prioritize shorter jobs
    sorted_jobs = sorted(jobs.keys(), key=lambda job_id: job_processing_times[job_id])


    for job_id in sorted_jobs:
        schedule[job_id] = []
        operations = jobs[job_id]
        
        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1
            
            # Find the machine that minimizes the makespan increase
            best_machine = None
            min_end_time = float('inf')
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id]) #Ensure sequence and machine constraints.
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine

            if best_machine is None: #Handle the case where no best machine can be determined
                 best_machine = machines[0]
                 processing_time = times[0]
                 start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
                 end_time = start_time + processing_time

            processing_time = times[machines.index(best_machine)] if best_machine in machines else times[0] #Processing time depends on chosen machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id]) #Ensure sequence and machine constraints.
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time #Machine is busy now
            machine_load[best_machine] += processing_time #Keep track of the total time a machine is used.
            job_completion_time[job_id] = end_time  #The job can only have the next operation executed after this one is complete.

    return schedule
