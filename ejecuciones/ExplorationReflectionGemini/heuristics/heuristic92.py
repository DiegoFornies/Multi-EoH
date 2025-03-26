
def heuristic(input_data):
    """FJSSP heuristic: Combines earliest availability & SPT on least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for op_idx, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]
            op_num = op_idx + 1

            best_machine = None
            min_completion_time = float('inf')
            least_loaded_machine = None
            min_load = float('inf')

            # Find least loaded machine
            for machine in possible_machines:
                if machine_load[machine] < min_load:
                    min_load = machine_load[machine]
                    least_loaded_machine = machine
            
            # Find machine with shortest processing time on the least loaded machine
            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                if machine == least_loaded_machine:
                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    end_time = start_time + processing_time

                    if end_time < min_completion_time:
                        min_completion_time = end_time
                        best_machine = machine
                        best_start_time = start_time
                        best_processing_time = processing_time
            
            #If for any reason no machine is selected, fallback to earliest availability
            if best_machine is None:
                for i in range(len(possible_machines)):
                    machine = possible_machines[i]
                    processing_time = possible_times[i]

                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    end_time = start_time + processing_time
                    if end_time < min_completion_time:
                      min_completion_time = end_time
                      best_machine = machine
                      best_start_time = start_time
                      best_processing_time = processing_time

            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
