
def heuristic(input_data):
    """Schedules jobs using a shifting bottleneck approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    remaining_operations = {}
    for job_id in jobs:
        remaining_operations[job_id] = list(range(len(jobs[job_id])))

    while any(remaining_operations.values()):
        #Identify the "bottleneck" machine with the most waiting time
        bottleneck_machine = None
        max_wait = -1
        for m in range(n_machines):
            wait_time = 0
            num_ops = 0
            for job_id, ops in jobs.items():
                if not remaining_operations[job_id]: continue
                op_idx = remaining_operations[job_id][0]
                machines, times = ops[op_idx]
                if m in machines:
                    num_ops += 1
                    idx = machines.index(m)
                    time = times[idx]
                    available_time = machine_available_times[m]
                    start_time = max(job_completion_times[job_id], available_time)
                    wait_time += start_time - job_completion_times[job_id]
            if num_ops > 0 and wait_time > max_wait:
                max_wait = wait_time
                bottleneck_machine = m

        #Schedule operations that can be performed on bottleneck first
        if bottleneck_machine is not None:
          scheduled_count = 0
          for job_id, ops in jobs.items():
              if not remaining_operations[job_id]: continue
              op_idx = remaining_operations[job_id][0]
              machines, times = ops[op_idx]

              if bottleneck_machine in machines:
                  idx = machines.index(bottleneck_machine)
                  processing_time = times[idx]
                  start_time = max(machine_available_times[bottleneck_machine], job_completion_times[job_id])
                  end_time = start_time + processing_time
                  schedule[job_id].append({
                      'Operation': op_idx + 1,
                      'Assigned Machine': bottleneck_machine,
                      'Start Time': start_time,
                      'End Time': end_time,
                      'Processing Time': processing_time
                  })
                  machine_available_times[bottleneck_machine] = end_time
                  job_completion_times[job_id] = end_time
                  remaining_operations[job_id].pop(0)
                  scheduled_count += 1

        #Schedule the rest on best available machine with SPT
        for job_id, ops in jobs.items():
            if not remaining_operations[job_id]: continue
            op_idx = remaining_operations[job_id][0]
            machines, times = ops[op_idx]

            if bottleneck_machine in machines: continue #Already scheduled

            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            for i, m in enumerate(machines):
                available_time = machine_available_times[m]
                start_time = max(job_completion_times[job_id], available_time)
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = m
                    processing_time = times[i]

            if best_machine is not None:
                start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                schedule[job_id].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_available_times[best_machine] = end_time
                job_completion_times[job_id] = end_time
                remaining_operations[job_id].pop(0)

    return schedule
