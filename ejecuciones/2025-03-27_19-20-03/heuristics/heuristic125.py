
def heuristic(input_data):
    """Combines min idle time and SPT for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_operations_left = {j: 0 for j in range(1, n_jobs + 1)}

    priority_queue = []
    for job in range(1, n_jobs + 1):
      ops = jobs_data[job]
      machines, times = ops[0]
      min_time = min(times)
      priority = min_time
      priority_queue.append((priority,job))
    priority_queue.sort()

    while priority_queue:
      priority, job = priority_queue.pop(0)
      if job not in schedule:
        schedule[job] = []

      op_idx = job_operations_left[job]
      machines, times = jobs_data[job][op_idx]

      best_machine = None
      min_idle_time = float('inf')
      best_processing_time = None

      for m_idx, machine in enumerate(machines):
          processing_time = times[m_idx]
          start_time = max(machine_available_time[machine], job_completion_time[job])
          idle_time = start_time - machine_available_time[machine] if start_time > machine_available_time[machine] else 0
          if idle_time < min_idle_time:
              min_idle_time = idle_time
              best_machine = machine
              best_processing_time = processing_time
              best_start_time = start_time

      start_time = best_start_time
      processing_time = best_processing_time
      end_time = start_time + processing_time

      schedule[job].append({
          'Operation': op_idx + 1,
          'Assigned Machine': best_machine,
          'Start Time': start_time,
          'End Time': end_time,
          'Processing Time': processing_time
      })

      machine_available_time[best_machine] = end_time
      job_completion_time[job] = end_time
      job_operations_left[job] += 1

      if job_operations_left[job] < len(jobs_data[job]):
          next_machines, next_times = jobs_data[job][job_operations_left[job]]
          min_time = min(next_times)
          priority = job_completion_time[job] + min_time
          priority_queue.append((priority, job))
          priority_queue.sort()

    return schedule
