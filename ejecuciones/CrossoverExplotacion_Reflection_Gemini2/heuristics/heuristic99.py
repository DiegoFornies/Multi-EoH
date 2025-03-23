
def heuristic(input_data):
    """
    Balances makespan, separation, and machine load. It uses SPT
    and considers machine workload. Delays assignments if needed.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}
    operation_start_times = {}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        earliest_start_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            min_start_time = float('inf')
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                min_start_time = min(min_start_time, start_time)

            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_job, best_op_index = job_id, op_index

        job_id, op_index = best_job, best_op_index
        machines, times = jobs_data[job_id][op_index]

        # Select machine with shortest processing time AND least workload
        best_machine, best_processing_time = None, float('inf')
        earliest_completion_time = float('inf')

        for machine_id, processing_time in zip(machines, times):
            available_time = machine_available_times[machine_id]
            start_time = max(available_time, job_completion_times[job_id])
            completion_time = start_time + processing_time
            workload = machine_workload[machine_id]

            # Prioritize less loaded machines with smaller completion times
            # Use a combined metric: completion time + workload factor
            combined_metric = completion_time + (workload / (sum(machine_workload.values()) + 1e-6)) * 5

            if combined_metric < earliest_completion_time:
                earliest_completion_time = combined_metric
                best_machine, best_processing_time = machine_id, processing_time

        # Introduce a delay mechanism
        delay_factor = 0.1  # Adjust this factor
        potential_start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        
        #calculate the average processing time among all the operations
        avg_processing_time = sum(times) / len(times)
        
        # If the current start time is too early, delay it
        # The condition checks if the current start time is very close to zero
        if potential_start_time < avg_processing_time / 2:
            potential_start_time = avg_processing_time / 2

        start_time = potential_start_time
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time

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
