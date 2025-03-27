
def heuristic(input_data):
    """Minimize makespan, reduce idle time, balance machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Adaptive Earliest Due Date (EDD) with machine consideration
    job_due_dates = {}
    for job in range(1, n_jobs + 1):
      total_processing_time = 0
      for operation in jobs_data[job]:
          total_processing_time += min(operation[1])
      job_due_dates[job] = total_processing_time  # Initial EDD proxy
        
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}
    
    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times, job))

        # Prioritize Adaptive EDD
        best_operation = None
        min_completion_time = float('inf')

        for job, op_num, machines, times, original_job in eligible_operations:

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                end_time = start_time + times[m_idx]
                
                # Adaptive EDD influence
                completion_time_weight = job_due_dates[original_job] + end_time
                
                if completion_time_weight < min_completion_time:
                    min_completion_time = completion_time_weight
                    best_operation = (job, op_num, m, start_time, times[m_idx], original_job)

        if best_operation:
            job, op_num, machine, start_time, processing_time, original_job = best_operation

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = start_time + processing_time
            job_completion_time[job] = start_time + processing_time

            remaining_operations[job].pop(0)
                
            #Adaptive EDD update
            job_due_dates[original_job] = job_completion_time[job] # update the due date for next selection

    return schedule
