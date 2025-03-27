
def heuristic(input_data):
    """
    A heuristic to solve the FJSSP, prioritizing machines with the least workload.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}  # Tracks the total load on each machine.
    machine_availability = {m: 0 for m in range(n_machines)} # Tracks when machine will be avail.
    job_completion = {j: 0 for j in range(1, n_jobs + 1)} # Tracks when job completes.

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        job_time = 0
        
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            
            # Find the machine with the least load among the feasible machines
            best_machine = None
            min_completion_time = float('inf')
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                completion_time = max(machine_availability[machine], job_completion[job]) + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine
            start_time = max(machine_availability[best_machine], job_completion[job])
            end_time = start_time + best_processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine load and available time, and job completion
            machine_load[best_machine] += best_processing_time
            machine_availability[best_machine] = end_time
            job_completion[job] = end_time

    return schedule
