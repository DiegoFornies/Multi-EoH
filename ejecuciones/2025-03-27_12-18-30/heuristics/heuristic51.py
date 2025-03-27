
def heuristic(input_data):
    """FJSSP heuristic: SPT with load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    
    remaining_operations = {}
    for job in range(1, n_jobs + 1):
      remaining_operations[job] = [(i+1, op) for i, op in enumerate(jobs_data[job])]
      
    while any(remaining_operations.values()):
      eligible_operations = []
      for job, ops in remaining_operations.items():
          if ops:
              eligible_operations.append((job, ops[0]))

      best_operation = None
      best_machine = None
      min_weighted_time = float('inf')
          
      for job, (op_num, (machines, times)) in eligible_operations:
          
          shortest_time = float('inf')
          chosen_machine = None
          
          for m_idx, m in enumerate(machines):
            time = times[m_idx]
            weighted_time = time + 0.1 * machine_load[m]
            if weighted_time < shortest_time:
              shortest_time = weighted_time
              chosen_machine = m
              processing_time = time # storing processing time from machine

          if chosen_machine is not None:
            start_time = max(machine_load[chosen_machine], job_completion_time[job])
            completion_time = start_time + processing_time

            if completion_time < min_weighted_time:
              min_weighted_time = completion_time
              best_operation = (job, (op_num, (machines, times)))
              best_machine = chosen_machine
              best_processing_time = processing_time
              
      if best_operation is not None and best_machine is not None:
        job, (op_num, (machines, times)) = best_operation
       
        start_time = max(machine_load[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time
            
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_load[best_machine] = end_time
        job_completion_time[job] = end_time
        remaining_operations[job].pop(0)
    
    return schedule
