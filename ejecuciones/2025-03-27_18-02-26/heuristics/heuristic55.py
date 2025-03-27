
def heuristic(input_data):
    """Schedules jobs by prioritizing shortest processing time."""
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {}
    
    # Create a list of all operations with their possible start times
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_idx, op_data in enumerate(operations_list):
            machines, processing_times = op_data
            min_processing_time = min(processing_times) if processing_times else float('inf')
            operations.append((job_id, op_idx, machines, processing_times, min_processing_time))
    
    # Sort operations by shortest processing time
    operations.sort(key=lambda x: x[4])  # Sort by min_processing_time
    
    for job_id, op_idx, machines, processing_times, _ in operations:
      if job_id not in schedule:
          schedule[job_id] = []

      # Find the machine that allows the earliest start for this operation.
      best_machine = None
      min_start_time = float('inf')
        
      for machine_idx, machine in enumerate(machines):
          start_time = max(machine_available_times[machine], job_completion_times[job_id])
          if start_time < min_start_time:
              min_start_time = start_time
              best_machine = machine
              best_processing_time = processing_times[machine_idx]
    
      start_time = min_start_time
      end_time = start_time + best_processing_time

      # Update machine availability and job completion time
      machine_available_times[best_machine] = end_time
      job_completion_times[job_id] = end_time
      
      schedule[job_id].append({
          'Operation': op_idx + 1,
          'Assigned Machine': best_machine,
          'Start Time': start_time,
          'End Time': end_time,
          'Processing Time': best_processing_time
      })
      
    return schedule
