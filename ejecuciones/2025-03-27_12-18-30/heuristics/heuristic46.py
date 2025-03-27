
def heuristic(input_data):
    """FJSSP heuristic: Earliest Due Date (EDD) with machine consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_due_date = {}
    for job in range(1, n_jobs + 1):
        job_due_date[job] = sum(min(times) for machines, times in jobs_data[job]) # sum of shortest processing times for all operations
        
    remaining_operations = {}
    for job in range(1, n_jobs + 1):
      remaining_operations[job] = [(i+1, op) for i, op in enumerate(jobs_data[job])]
      
    scheduled_operations = []
    while any(remaining_operations.values()):
      eligible_operations = []
      for job, ops in remaining_operations.items():
          if ops:
              eligible_operations.append((job, ops[0]))  # (job, (op_num, (machines, times)))
      
      if not eligible_operations:
          break  # No more operations to schedule

      # Sort eligible operations by EDD
      eligible_operations.sort(key=lambda x: job_due_date[x[0]])
          
      for job, (op_num, (machines, times)) in eligible_operations:
          shortest_time = float('inf')
          chosen_machine = None
          
          for m_idx, m in enumerate(machines):
            time = times[m_idx]
            if machine_available_time[m] + time < shortest_time: # check which machines make job finished soonest
                shortest_time = machine_available_time[m] + time
                chosen_machine = m
                processing_time = time
            
          if chosen_machine is not None:
            start_time = machine_available_time[chosen_machine]
            end_time = start_time + processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': chosen_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[chosen_machine] = end_time
            remaining_operations[job].pop(0)
            break
    return schedule
