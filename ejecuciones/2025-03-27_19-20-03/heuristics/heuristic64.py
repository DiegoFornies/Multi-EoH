
def heuristic(input_data):
    """Schedules jobs using Shortest Processing Time (SPT) on each machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    # Iterate through operations of each job, assigning them to machines.
    for job in range(1, n_jobs + 1):
      current_time=0
      for op_idx, (machines, times) in enumerate(jobs[job]):
        op_num = op_idx+1
        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for m_idx, machine in enumerate(machines):
          #Earliest Finish Time for current machine and operation
          start_time = max(machine_available_time[machine], current_time)
          end_time = start_time + times[m_idx]

          if end_time < min_end_time:
            min_end_time = end_time
            best_machine = machine
            processing_time = times[m_idx]

        if best_machine is not None:
            start_time = max(machine_available_time[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job].append({
              'Operation': op_num,
              'Assigned Machine': best_machine,
              'Start Time': start_time,
              'End Time': end_time,
              'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time
        else:
          raise ValueError("No machine is suitable for schedule!")
    return schedule
