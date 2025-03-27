
def heuristic(input_data):
    """Combines minimizing idle time and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    remaining_operations = {job: [i for i in range(len(ops))] for job, ops in jobs.items()}

    available_operations = []
    for job in jobs:
      if remaining_operations[job]:
        available_operations.append((job,remaining_operations[job][0]))
    
    while available_operations:
      best_op = None
      earliest_start = float('inf')

      for job, op_idx in available_operations:
        machines, times = jobs[job][op_idx]
        
        best_machine = None
        min_start_time = float('inf')
        min_load_machine = None
        min_load = float('inf')
        best_load_time = None

        for m_idx, m in enumerate(machines):
          start_time = max(machine_time[m], job_completion_time[job])
          if start_time < min_start_time:
            min_start_time = start_time
            best_machine = m
            best_time = times[m_idx]
          
          load = machine_load[m]
          if load < min_load:
              min_load = load
              min_load_machine = m
              best_load_time = times[m_idx]

        #prefer the earliest start or min load
        if min_start_time <= earliest_start:
          earliest_start = min_start_time
          best_op = (job, op_idx, best_machine, best_time, min_start_time)
        elif min_load < float('inf') and machine_time[min_load_machine] <= earliest_start :
            best_op = (job, op_idx, min_load_machine, best_load_time, max(machine_time[min_load_machine], job_completion_time[job]))

      if best_op is None:
          continue

      job, op_idx, assigned_machine, processing_time, start_time = best_op

      end_time = start_time + processing_time

      if job not in schedule:
        schedule[job] = []
      
      schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
      })
      
      remaining_operations[job].pop(0)
      
      machine_time[assigned_machine] = end_time
      machine_load[assigned_machine] += processing_time
      job_completion_time[job] = end_time

      if remaining_operations[job]:
        available_operations.append((job, remaining_operations[job][0]))

      available_operations.remove((job, op_idx))

    return schedule
