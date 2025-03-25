
def heuristic(input_data):
    """A two-phase heuristic: Greedy makespan, then balance refinement."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

    # Phase 1: Greedy Makespan
    while available_operations:
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    # Phase 2: Balance Refinement (Simple Swap)
    # This is a simplified example, more advanced local search can be implemented.
    for _ in range(n_jobs): #Iterate as many times as there are jobs
      job_id1 = _ % n_jobs + 1
      if len(schedule[job_id1]) > 1:
        op_idx = len(schedule[job_id1]) -1
        current_machine = schedule[job_id1][op_idx]['Assigned Machine']

        machines, times = jobs[job_id1][op_idx]
        #Find a better machine to balance load
        best_machine = current_machine
        best_start_time = schedule[job_id1][op_idx]['Start Time']

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id1])

            if machine != current_machine and start_time < best_start_time:
              best_start_time = start_time
              best_machine = machine
        if best_machine != current_machine:
          processing_time = times[machines.index(best_machine)]
          start_time = max(machine_available_time[best_machine], job_completion_time[job_id1])
          end_time = start_time + processing_time

          machine_available_time[current_machine] -= schedule[job_id1][op_idx]['Processing Time']
          machine_available_time[best_machine] = end_time
          
          schedule[job_id1][op_idx]['Assigned Machine'] = best_machine
          schedule[job_id1][op_idx]['Start Time'] = start_time
          schedule[job_id1][op_idx]['End Time'] = end_time
          schedule[job_id1][op_idx]['Processing Time'] = processing_time
          
          machine_available_time = {m: 0 for m in range(n_machines)}
          job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
          for job_id in range(1, n_jobs + 1):
            for op in schedule[job_id]:
              machine_available_time[op['Assigned Machine']] = max(machine_available_time[op['Assigned Machine']], op['End Time'])
              job_completion_time[job_id] = max(job_completion_time[job_id], op['End Time'])
    return schedule
