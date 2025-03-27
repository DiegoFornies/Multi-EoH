
def heuristic(input_data):
    """Heuristic for FJSSP: Shortest Remaining Processing Time & Machine Load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_remaining_times = {}

    for job_id in jobs:
        schedule[job_id] = []
        remaining_time = 0
        for operation in jobs[job_id]:
            remaining_time += min(operation[1])
        job_remaining_times[job_id] = remaining_time

    completed_operations = {job_id: 0 for job_id in range(1, n_jobs + 1)}
    eligible_operations = []

    for job_id in jobs:
      eligible_operations.append((job_id, 0))

    while eligible_operations:
      best_operation = None
      best_job = None
      best_machine = None
      min_completion_time = float('inf')
      
      for job_id, op_index in eligible_operations:
        operation = jobs[job_id][op_index]
        possible_machines = operation[0]
        possible_times = operation[1]

        for machine_index, machine_id in enumerate(possible_machines):
          processing_time = possible_times[machine_index]
          start_time = max(machine_available_times[machine_id],
                            (schedule[job_id][-1]['End Time'] if schedule[job_id] else 0) if op_index > 0 else 0) #Respecting job sequence

          completion_time = start_time + processing_time
          
          if completion_time < min_completion_time:
            min_completion_time = completion_time
            best_operation = op_index
            best_job = job_id
            best_machine = machine_id
            best_processing_time = processing_time
            best_start_time = start_time

      schedule.setdefault(best_job, [])
      schedule[best_job].append({
        'Operation': best_operation + 1,
        'Assigned Machine': best_machine,
        'Start Time': best_start_time,
        'End Time': best_start_time + best_processing_time,
        'Processing Time': best_processing_time
      })

      machine_available_times[best_machine] = best_start_time + best_processing_time
      job_remaining_times[best_job] -= best_processing_time
      
      eligible_operations.remove((best_job, best_operation))
      if best_operation+1 < len(jobs[best_job]):
        eligible_operations.append((best_job, best_operation+1))
    return schedule
