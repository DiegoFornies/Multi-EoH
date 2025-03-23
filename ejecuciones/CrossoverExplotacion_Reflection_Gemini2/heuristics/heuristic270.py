
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing workload."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id in jobs_data:
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine = None
        min_combined_metric = float('inf')

        for job_id, op_index in ready_operations:
            machines, processing_times = jobs_data[job_id][op_index]

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time

                # Combine makespan and workload considerations
                workload_factor = machine_workload[machine]
                combined_metric = end_time + 0.1 * workload_factor  # Adjust weight as needed

                if combined_metric < min_combined_metric:
                    min_combined_metric = combined_metric
                    best_job = job_id
                    best_op_index = op_index
                    best_machine = machine
                    best_processing_time = processing_time


        job_id, op_index = best_job, best_op_index
        start_time = max(machine_available[best_machine], job_completion[job_id])
        end_time = start_time + best_processing_time
        machine_available[best_machine] = end_time
        job_completion[job_id] = end_time
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
