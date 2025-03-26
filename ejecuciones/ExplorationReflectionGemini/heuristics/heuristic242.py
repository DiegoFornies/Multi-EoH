
def heuristic(input_data):
    """Combines SPT and least-loaded machine, adapting based on job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    job_operation_indices = {job_id: 0 for job_id in range(1, n_jobs + 1)}

    completed_jobs = 0
    while completed_jobs < n_jobs:
        available_operations = []
        for job_id in range(1, n_jobs + 1):
            if job_operation_indices[job_id] < len(jobs[job_id]):
                available_operations.append(job_id)

        best_job = None
        best_machine = None
        best_processing_time = float('inf')
        best_start_time = float('inf')
        
        for job_id in available_operations:
            operation_index = job_operation_indices[job_id]
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            least_loaded_machine = None
            min_load = float('inf')

            for machine in possible_machines:
                 if machine_load[machine] < min_load:
                    min_load = machine_load[machine]
                    least_loaded_machine = machine

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                if machine == least_loaded_machine:
                    start_time = max(machine_available_times[machine], job_completion_times[job_id])
                    if start_time < best_start_time or (start_time == best_start_time and processing_time < best_processing_time):
                        best_job = job_id
                        best_machine = machine
                        best_processing_time = processing_time
                        best_start_time = start_time
        
        if best_job is None:
          break

        operation_index = job_operation_indices[best_job]
        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_processing_time

        schedule[best_job].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_times[best_machine] = end_time
        machine_load[best_machine] += best_processing_time
        job_completion_times[best_job] = end_time
        job_operation_indices[best_job] += 1

        if job_operation_indices[best_job] == len(jobs[best_job]):
            completed_jobs += 1

    return schedule
