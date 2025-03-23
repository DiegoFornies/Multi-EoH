
def heuristic(input_data):
    """Schedules jobs minimizing makespan, separation, and balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}
    job_starts = {j: [] for j in range(1, n_jobs + 1)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            # Early Separation Prioritization
            potential_starts = []
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                potential_starts.append((machine_id, start_time, processing_time))
            
            # Calculate separation cost, prioritize large seperation
            best_potential_start = None
            max_separation = -1

            for machine_id, start_time, processing_time in potential_starts:

                completion_time = start_time + processing_time
                separation_cost = 0

                if len(job_starts[job_id])>0:
                    separation_cost = start_time - job_starts[job_id][-1] # how much separation between operations
                
                if separation_cost > max_separation:
                    max_separation = separation_cost
                    best_potential_start = (machine_id,start_time,processing_time)

            machine_id, start_time, processing_time = best_potential_start

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_job, best_op_index = job_id, op_index
                best_machine = machine_id
                best_processing_time = processing_time

        job_id, op_index = best_job, best_op_index
        best_machine = best_machine
        best_processing_time = best_processing_time
        start_time = earliest_start_time

        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time
        job_starts[job_id].append(start_time)

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
