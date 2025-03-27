
def heuristic(input_data):
    """
    Hybrid approach: EDD, SPT, and adaptive load balancing
    to minimize makespan while maintaining balance.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    job_due_dates = {} #Placeholder for EDD
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}

    # Calculate job due dates (Earliest Due Date)
    for job in range(1, n_jobs + 1):
      total_processing_time = 0
      for operation in jobs_data[job]:
        total_processing_time += min(operation[1]) #Min processing time
      job_due_dates[job] = total_processing_time
    
    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))
        
    while eligible_operations:
        # Prioritize operations using a weighted score (EDD + SPT + Load)
        best_op = None
        best_score = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                processing_time = times[m_idx]

                #EDD component
                edd_weight = 0.5
                edd_component = edd_weight * job_due_dates[job]

                #SPT component
                spt_weight = 0.3
                spt_component = spt_weight * processing_time
                
                #Load Balancing component
                load_weight = 0.2
                load_component = load_weight * machine_available_times[m]
                               
                total_score = start_time + spt_component + load_component - edd_component

                if total_score < best_score:
                    best_score = total_score
                    best_op = op_num
                    best_machine = m
                    best_time = processing_time
                    best_job = job
                    
        # Schedule operation
        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_time

        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time
        
        eligible_operations.remove((best_job, best_op))
        
        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
