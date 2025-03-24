
def heuristic(input_data):
    """Combines min-workload machine selection with earliest-start priority."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {machine: 0 for machine in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
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
              start_time = max(machine_load[machine], job_completion_times[job])

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

        start_time = max(machine_load[machine], job_completion_times[best_job])
        end_time = start_time + processing_time

        schedule[best_job].append({
            'Operation': best_op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        # Update machine and job completion times
        machine_load[machine] = end_time
        job_completion_times[best_job] = end_time
        
        if len(schedule[best_job]) == len(jobs[best_job]):
            job_sequence.remove(best_job)
    return schedule
