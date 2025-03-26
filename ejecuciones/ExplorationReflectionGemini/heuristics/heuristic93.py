
def heuristic(input_data):
    """Schedules jobs using SPT and least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_start_time = float('inf')
            min_processing_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                if processing_time < min_processing_time:
                  min_processing_time = processing_time
                  min_start_time = start_time
                  best_machine = machine
                elif processing_time == min_processing_time and start_time < min_start_time:
                  min_start_time = start_time
                  best_machine = machine
            
            best_processing_time = 0
            for i, machine in enumerate(machines):
              if machine == best_machine:
                best_processing_time = times[i]

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': min_start_time,
                'End Time': min_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = min_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = min_start_time + best_processing_time

    return schedule
