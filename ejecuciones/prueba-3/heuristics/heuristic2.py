
def heuristic(input_data):
    """Schedules jobs using a machine load balancing approach."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in jobs}

    for job in jobs:
        schedule[job] = []

    # Iterate through operations, assigning to least loaded machine
    op_idx = 0
    unassigned_ops = {}
    for job_id, operations in jobs.items():
          unassigned_ops[job_id] = 0


    is_all_jobs_done = False
    while not is_all_jobs_done:
      is_all_jobs_done = True
      for job_id, operations in jobs.items():
        if unassigned_ops[job_id] < len(operations):
          is_all_jobs_done = False #at least one job is not done

          machines, times = operations[unassigned_ops[job_id]]

          # Find the machine with the earliest available time for this operation.
          best_machine = None
          min_end_time = float('inf')
          proc_time = -1

          for i in range(len(machines)):
            m = machines[i]
            t = times[i]
            start_time = max(machine_load[m], job_completion[job_id])
            end_time = start_time + t

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                proc_time = t


          start_time = max(machine_load[best_machine], job_completion[job_id])
          end_time = start_time + proc_time
          
          schedule[job_id].append({
              'Operation': unassigned_ops[job_id]+1,
              'Assigned Machine': best_machine,
              'Start Time': start_time,
              'End Time': end_time,
              'Processing Time': proc_time
          })

          # Update machine load and job completion time.
          machine_load[best_machine] = end_time
          job_completion[job_id] = end_time
          unassigned_ops[job_id] +=1
                
    return schedule
