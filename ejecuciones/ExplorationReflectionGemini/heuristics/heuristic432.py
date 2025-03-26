
def heuristic(input_data):
    """Combines SPT and least loaded machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_processing_time = float('inf')

            # Find the shortest processing time on least loaded machine.
            least_loaded_machine = None
            min_load = float('inf')
            for machine in possible_machines:
                if machine_load[machine] < min_load:
                    min_load = machine_load[machine]
                    least_loaded_machine = machine
            
            # Prefer the least loaded machine
            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                if machine == least_loaded_machine: #prefer least loaded
                  if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine
                    best_processing_time = processing_time
                    
            if best_machine is None:
                best_machine = possible_machines[0]
                best_processing_time = possible_times[0]
                

            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_times[job_id] = end_time

    return schedule
