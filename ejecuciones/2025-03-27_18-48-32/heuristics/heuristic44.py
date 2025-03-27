
def heuristic(input_data):
    """Schedules jobs, balancing machine load and job completion."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_ops = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
      schedule[job] = []
      remaining_ops[job] = 0

    op_queue = []
    for job_id in range(1, n_jobs + 1):
        ops = jobs[job_id]
        machines, times = ops[0]
        op_queue.append((job_id, 0, machines, times))

    while op_queue:
      best_op = None
      min_makespan = float('inf')
      # find the best op according to machine load & min makespan
      for job_id, op_idx, machines, times in op_queue:
        for m_idx, m in enumerate(machines):
          start_time = max(machine_load[m], job_completion[job_id])
          end_time = start_time + times[m_idx]
          if end_time < min_makespan:
            min_makespan = end_time
            best_op = (job_id, op_idx, m, times[m_idx])

      # schedule best operation
      job_id, op_idx, machine, time = best_op
      start_time = max(machine_load[machine], job_completion[job_id])
      end_time = start_time + time

      schedule[job_id].append({
          'Operation': op_idx + 1,
          'Assigned Machine': machine,
          'Start Time': start_time,
          'End Time': end_time,
          'Processing Time': time
      })

      machine_load[machine] = end_time
      job_completion[job_id] = end_time

      op_queue.remove((job_id, op_idx, jobs[job_id][op_idx][0], jobs[job_id][op_idx][1]))

      next_op_index = op_idx + 1
      if next_op_index < len(jobs[job_id]):
        machines, times = jobs[job_id][next_op_index]
        op_queue.append((job_id, next_op_index, machines, times))

    return schedule
