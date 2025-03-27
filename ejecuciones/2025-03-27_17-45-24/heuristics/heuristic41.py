
def heuristic(input_data):
    """Combines EFT and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        job_completion_time = 0

        for op_index, operation in enumerate(jobs[job]):
            machines, times = operation
            best_machine, best_start_time, best_processing_time = None, float('inf'), None

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time)
                end_time = start_time + processing_time
                load_factor = machine_load[machine]

                if end_time + load_factor < best_start_time:
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
            
            operation_data = {
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            }
            schedule[job].append(operation_data)
            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time = best_start_time + best_processing_time

    return schedule
