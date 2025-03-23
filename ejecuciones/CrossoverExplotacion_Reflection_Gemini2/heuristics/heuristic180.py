
def heuristic(input_data):
    """Schedules jobs focusing on initial separation to minimize makespan later."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    # Initial Separation Phase (Strategic Delay)
    initial_delay = {}
    for job_id in range(1, n_jobs + 1):
        initial_delay[job_id] = 0
    makespan_estimate = 0

    while ready_operations:
        best_job, best_op_index = None, None
        earliest_start_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            min_start_time = float('inf')
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time + initial_delay[job_id], job_completion_times[job_id])  # Apply initial delay
                min_start_time = min(min_start_time, start_time)

            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_job, best_op_index = job_id, op_index

        job_id, op_index = best_job, best_op_index
        machines, times = jobs_data[job_id][op_index]

        # Select machine with shortest processing time AND least workload, factoring in delay
        best_machine, best_processing_time = None, float('inf')
        earliest_completion_time = float('inf')

        for machine_id, processing_time in zip(machines, times):
            available_time = machine_available_times[machine_id]
            start_time = max(available_time + initial_delay[job_id], job_completion_times[job_id])  # Apply initial delay
            completion_time = start_time + processing_time
            workload = machine_workload[machine_id]

            # Delay factor based on current makespan and workload
            # Current makespan adjusted for initial delay, to reflect a forward-looking state
            current_makespan = max(machine_available_times.values())
            delay_factor = (workload / (sum(machine_workload.values()) + 1e-6)) * (completion_time / (current_makespan + 1e-6)) * 5

            combined_metric = completion_time + (workload / (sum(machine_workload.values()) + 1e-6)) * 5 + delay_factor

            if combined_metric < earliest_completion_time:
                earliest_completion_time = combined_metric
                best_machine, best_processing_time = machine_id, processing_time

        start_time = max(machine_available_times[best_machine] + initial_delay[job_id], job_completion_times[job_id])  # Apply initial delay
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time
        makespan_estimate = max(makespan_estimate, end_time)

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

        # Dynamically adjust initial delay based on job completion time
        # and an estimate of the makespan, so early jobs have a longer delay
        initial_delay[job_id] = (makespan_estimate - end_time) / (n_jobs + 1)

    return schedule
