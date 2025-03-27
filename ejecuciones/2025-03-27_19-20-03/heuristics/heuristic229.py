
def heuristic(input_data):
    """Schedules jobs to minimize makespan using a shortest processing time (SPT) based approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    
    available_ops = []
    for job in jobs:
      available_ops.append((min(jobs[job][0][1]), job))

    while available_ops:
      available_ops.sort()
      _, job = available_ops.pop(0)

      if job not in schedule:
        schedule[job] = []

      op_idx = job_ops[job]
      machines, times = jobs[job][op_idx]

      best_machine = None
      min_end_time = float('inf')
      best_time = None
      
      for m, t in zip(machines, times):
        start_time = max(machine_time[m], job_completion_time[job])
        end_time = start_time + t
        if end_time < min_end_time:
          min_end_time = end_time
          best_machine = m
          best_time = t

      start_time = max(machine_time[best_machine], job_completion_time[job])
      end_time = start_time + best_time

      schedule[job].append({
          'Operation': op_idx + 1,
          'Assigned Machine': best_machine,
          'Start Time': start_time,
          'End Time': end_time,
          'Processing Time': best_time
      })

      machine_time[best_machine] = end_time
      job_completion_time[job] = end_time
      job_ops[job] += 1

      if job_ops[job] < len(jobs[job]):
          min_time = min(jobs[job][job_ops[job]][1])
          available_ops.append((min_time, job))
          available_ops.sort()

    return schedule
