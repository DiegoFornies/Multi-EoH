
def heuristic(input_data):
    """Combines SPT, machine load, and job completion for FJSSP with workload balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    
    ready_operations = []
    for job_id in jobs:
      ready_operations.append((job_id, 0))

    while ready_operations:
      best_job, best_op_index = None, None
      min_combined_score = float('inf')

      for job_id, op_index in ready_operations:
          machines, times = jobs[job_id][op_index]

          for m_idx, machine in enumerate(machines):
              processing_time = times[m_idx]
              start_time = max(machine_available_time[machine], job_completion_time[job_id])
              end_time = start_time + processing_time

              # SPT, machine load, Job Completion, and Load Balance scoring
              load_penalty = machine_load[machine] / (sum(machine_load.values()) + 1e-6) if sum(machine_load.values()) > 0 else 0
              score = 0.4 * processing_time + 0.3 * machine_load[machine] + 0.2 * end_time + 0.1 * load_penalty

              if score < min_combined_score:
                  min_combined_score = score
                  best_job = job_id
                  best_op_index = op_index
                  best_machine = machine
                  best_processing_time = processing_time
                  best_start_time = start_time

      job_id, op_index = best_job, best_op_index
      best_machine = best_machine
      best_processing_time = best_processing_time
      best_start_time = best_start_time
      op_num = op_index + 1

      schedule[job_id] = schedule.get(job_id, [])
      schedule[job_id].append({
          'Operation': op_num,
          'Assigned Machine': best_machine,
          'Start Time': best_start_time,
          'End Time': best_start_time + best_processing_time,
          'Processing Time': best_processing_time
      })

      machine_load[best_machine] = best_start_time + best_processing_time
      machine_available_time[best_machine] = best_start_time + best_processing_time
      job_completion_time[job_id] = best_start_time + best_processing_time

      ready_operations.remove((job_id, op_index))

      if op_index + 1 < len(jobs[job_id]):
          ready_operations.append((job_id, op_index + 1))

    return schedule
