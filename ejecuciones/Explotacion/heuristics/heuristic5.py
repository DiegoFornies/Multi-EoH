
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time and balancing machine load
    by considering available machines and processing times to find the earliest available slot.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Store the schedule for each job
    machine_available_time = {m: 0 for m in range(n_machines)}  # Earliest available time for each machine
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}  # Completion time of each job

    for job in jobs:
        schedule[job] = []

    # Iterate through jobs and their operations
    job_sequence = list(jobs.keys()) # create the order of job processing
    
    while len(job_sequence) > 0:
      best_job = None
      earliest_start = float('inf')
      best_machine = None
      best_op_idx = None
      best_processing_time = None

      for job in job_sequence:
          ops = jobs[job]
          op_idx = len(schedule[job])
          if op_idx < len(ops): #Process one operation per job in a cycle
            machines, times = ops[op_idx]

            # Find the earliest available time slot for this operation
            for machine_index in range(len(machines)):
              machine = machines[machine_index]
              processing_time = times[machine_index]
              start_time = max(machine_available_time[machine], job_completion_time[job])

              if start_time < earliest_start:
                earliest_start = start_time
                best_job = job
                best_machine = machine
                best_op_idx = op_idx
                best_processing_time = processing_time
              
      if best_job is not None:
        ops = jobs[best_job]
        machines, times = ops[best_op_idx]
        processing_time = best_processing_time
        machine = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[best_job])
        end_time = start_time + processing_time

        schedule[best_job].append({
            'Operation': best_op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        # Update machine and job completion times
        machine_available_time[machine] = end_time
        job_completion_time[best_job] = end_time
        
        if len(schedule[best_job]) == len(jobs[best_job]):
            job_sequence.remove(best_job)
    return schedule
