
def heuristic(input_data):
    """Heuristic for FJSSP, prioritizing makespan and balance with local search."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Initial greedy scheduling based on makespan and balance
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

    while available_operations:
        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        min_load = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                #Prioritize min makespan and machine load
                if start_time < best_start_time or (start_time == best_start_time and machine_load[machine] < min_load):

                    best_start_time = start_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)
                    min_load = machine_load[machine]
                    

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
        machine_load[machine] += processing_time
        available_operations.remove((job_id, op_idx))

        # Add the next operation of the job if it exists
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    # Local search (swap machines for operations to improve balance)
    for job_id in range(1, n_jobs + 1):
      for i in range(len(schedule[job_id])):
        operation = schedule[job_id][i]
        original_machine = operation['Assigned Machine']
        original_start_time = operation['Start Time']
        original_processing_time = operation['Processing Time']
        original_end_time = operation['End Time']

        job_op_idx = operation['Operation'] -1
        machines, times = jobs[job_id][job_op_idx]
        
        #Try other possible machines
        for machine_idx, machine in enumerate(machines):
            if machine != original_machine:
              processing_time = times[machine_idx]
              start_time = max(machine_available_time[machine] - original_processing_time if machine_available_time[machine] - original_processing_time > 0 else 0, job_completion_time[job_id] - original_processing_time if job_completion_time[job_id] - original_processing_time > 0 else 0)
              end_time = start_time + processing_time
              
              # Calculate new machine load
              new_machine_load = {m: 0 for m in range(n_machines)}
              temp_schedule = {}
              for k in range(1, n_jobs + 1):
                temp_schedule[k] = []

              temp_machine_available_time = {m: 0 for m in range(n_machines)}
              temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
              
              for k in range(1, n_jobs + 1):
                for operation_index in range(len(schedule[k])):
                  if k == job_id and operation_index == i:
                    temp_schedule[k].append({
                      'Operation': operation_index+1,
                      'Assigned Machine': machine,
                      'Start Time': start_time,
                      'End Time': end_time,
                      'Processing Time': processing_time
                    })
                    temp_machine_available_time[machine] = end_time
                    temp_job_completion_time[k] = end_time
                  else:
                    temp_schedule[k].append(schedule[k][operation_index])
                    temp_machine_available_time[schedule[k][operation_index]['Assigned Machine']] = schedule[k][operation_index]['End Time']
                    temp_job_completion_time[k] = schedule[k][operation_index]['End Time']

              #Check balance
              balance_before = sum(machine_load.values())/len(machine_load)
              machine_load[original_machine] -= original_processing_time
              machine_load[machine] += processing_time
              balance_after = sum(machine_load.values())/len(machine_load)
              if abs(machine_load[machine] - balance_after) < abs(machine_load[original_machine] - balance_before):
                  operation['Assigned Machine'] = machine
                  operation['Start Time'] = start_time
                  operation['End Time'] = end_time
                  operation['Processing Time'] = processing_time
                  
                  machine_available_time[original_machine] -= original_processing_time
                  machine_available_time[machine] += processing_time
                  break # Break after the first improved machine is found
              else:
                machine_load[original_machine] += original_processing_time
                machine_load[machine] -= processing_time

    return schedule
