
def heuristic(input_data):
    """Schedules jobs to minimize makespan, considering machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}  # Track machine load

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = op_num
                    best_machine = m
                    best_time = times[m_idx]
                    best_job = job
        
        #Machine balancing consideration - machine with least load
        available_machines = []
        for job, op_num in eligible_operations:
            if job == best_job and op_num == best_op:
                machines, times = jobs_data[job][op_num - 1]
                available_machines = machines
                processing_times = times
                break;
        
        lowest_load = float('inf')
        best_machine_balanced = best_machine
        best_time_balanced = best_time

        for idx, machine in enumerate(available_machines):
          start_time_alt = max(machine_available_times[machine], job_completion_times[best_job])
          if machine_load[machine] < lowest_load:
              lowest_load = machine_load[machine]
              best_machine_balanced = machine
              best_time_balanced = processing_times[idx]

        start_time = max(machine_available_times[best_machine_balanced], job_completion_times[best_job])
        end_time = start_time + best_time_balanced
        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine_balanced,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time_balanced
        })

        machine_available_times[best_machine_balanced] = end_time
        job_completion_times[best_job] = end_time
        machine_load[best_machine_balanced] += best_time_balanced #increase load

        eligible_operations.remove((best_job, best_op))

        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
