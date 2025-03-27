
def heuristic(input_data):
    """A heuristic for FJSSP, prioritizes shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            
            # Sort machines by processing time, shortest first
            machine_time_pairs = sorted(zip(machines, times), key=lambda x: x[1])

            best_machine = None
            best_processing_time = None
            start_time = None

            for machine, processing_time in machine_time_pairs:
                available_time = max(machine_load[machine], job_completion_time[job])
                
                best_machine = machine
                best_processing_time = processing_time
                start_time = available_time
                break #Take the shortest one immediately
                

            end_time = start_time + best_processing_time
            job_schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine,
                                    'Start Time': start_time, 'End Time': end_time,
                                    'Processing Time': best_processing_time})

            machine_load[best_machine] = end_time
            job_completion_time[job] = end_time

    return job_schedule
