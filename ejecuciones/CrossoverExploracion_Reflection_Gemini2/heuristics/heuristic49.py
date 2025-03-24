
def heuristic(input_data):
    """
    A heuristic for FJSSP that combines earliest start time and shortest processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    remaining_operations = {j: len(jobs[j]) for j in jobs}

    while sum(remaining_operations.values()) > 0:
      best_job = None
      best_machine = None
      earliest_start_time = float('inf')
      shortest_processing_time = float('inf')

      for job in range(1, n_jobs + 1):
        if remaining_operations[job] > 0:
          op_idx = len(schedule[job])
          machines, times = jobs[job][op_idx]

          for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]

            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < earliest_start_time or (start_time == earliest_start_time and processing_time < shortest_processing_time):
              best_job = job
              best_machine = machine
              earliest_start_time = start_time
              shortest_processing_time = processing_time
              best_processing_time = processing_time

      op_idx = len(schedule[best_job]) + 1
      start_time = earliest_start_time
      end_time = start_time + best_processing_time

      schedule[best_job].append({
          'Operation': op_idx,
          'Assigned Machine': best_machine,
          'Start Time': start_time,
          'End Time': end_time,
          'Processing Time': best_processing_time
      })

      machine_available_time[best_machine] = end_time
      job_completion_time[best_job] = end_time
      remaining_operations[best_job] -= 1

    return schedule
