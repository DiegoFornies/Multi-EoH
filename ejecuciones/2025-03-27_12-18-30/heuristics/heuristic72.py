
def heuristic(input_data):
    """Combines earliest start time and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    remaining_operations = {}
    for job in range(1, n_jobs + 1):
      remaining_operations[job] = [(i+1, op) for i, op in enumerate(jobs[job])]
      
    scheduled_operations = []
    while any(remaining_operations.values()):
      eligible_operations = []
      for job, ops in remaining_operations.items():
          if ops:
              eligible_operations.append((job, ops[0]))  # (job, (op_num, (machines, times)))
      
      if not eligible_operations:
          break  # No more operations to schedule

      best_operation = None
      best_machine = None
      min_completion_time = float('inf')
      
      for job, (op_num, (machines, times)) in eligible_operations:
        best_load_score = float('inf')
        chosen_machine = None
        shortest_time = float('inf')
        earliest_start_time = float('inf')
        
        for m_idx, m in enumerate(machines):
          time = times[m_idx]
          start_time = max(machine_available_time[m], job_completion_time[job])
          completion_time = start_time + time
          load_score = machine_load[m] + time

          if start_time < earliest_start_time:
            earliest_start_time = start_time
            best_load_score = load_score
            chosen_machine = m
            shortest_time = time
          elif start_time == earliest_start_time and load_score < best_load_score:
              best_load_score = load_score
              chosen_machine = m
              shortest_time = time

        if chosen_machine is not None:
          start_time = max(machine_available_time[chosen_machine], job_completion_time[job])
          completion_time = start_time + shortest_time
          
          if completion_time < min_completion_time:
            min_completion_time = completion_time
            best_operation = (job, (op_num, (machines, times)))
            best_machine = chosen_machine
      
      if best_operation is not None and best_machine is not None:
        job, (op_num, (machines, times)) = best_operation
        
        m_idx = jobs[job][op_num-1][0].index(best_machine) if best_machine in jobs[job][op_num-1][0] else 0
        processing_time = jobs[job][op_num-1][1][m_idx]

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time
            
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += processing_time
        job_completion_time[job] = end_time
        remaining_operations[job].pop(0)
    
    return schedule
