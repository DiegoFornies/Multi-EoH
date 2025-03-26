
def heuristic(input_data):
    """SPT on least loaded, considers job criticality."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    job_remaining_ops = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    scheduled_operations = 0
    total_operations = sum(len(jobs[j]) for j in range(1, n_jobs + 1))

    while scheduled_operations < total_operations:
      eligible_operations = []
      for job_id in range(1, n_jobs + 1):
        if job_remaining_ops[job_id] > 0:
          op_idx = len(schedule[job_id])
          eligible_operations.append((job_id, op_idx))
      
      #Determine best operation
      best_op = None
      min_start_time = float('inf')
      
      for job_id, op_idx in eligible_operations:
        operation_data = jobs[job_id][op_idx]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        best_machine_local = None
        min_processing_time = float('inf')
        least_loaded_machine = None
        min_load = float('inf')
        
        for machine in possible_machines:
             if machine_load[machine] < min_load:
                min_load = machine_load[machine]
                least_loaded_machine = machine

        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]
            
            if machine == least_loaded_machine: 
              if processing_time < min_processing_time:
                min_processing_time = processing_time
                best_machine_local = machine
                best_processing_time = processing_time
        
        start_time = max(machine_load[best_machine_local], job_completion_times[job_id])
        if start_time < min_start_time:
          min_start_time = start_time
          best_op = (job_id, op_idx, best_machine_local, best_processing_time)
      
      #Schedule the operation
      job_id, op_idx, best_machine, best_processing_time = best_op
      start_time = max(machine_load[best_machine], job_completion_times[job_id])
      end_time = start_time + best_processing_time

      schedule[job_id].append({
          'Operation': op_idx + 1,
          'Assigned Machine': best_machine,
          'Start Time': start_time,
          'End Time': end_time,
          'Processing Time': best_processing_time
      })
      
      machine_load[best_machine] = end_time
      job_completion_times[job_id] = end_time
      job_remaining_ops[job_id] -= 1
      scheduled_operations += 1
    
    return schedule
