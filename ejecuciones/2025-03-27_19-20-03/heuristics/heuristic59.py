
def heuristic(input_data):
    """Schedules jobs using a global makespan estimation."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    
    operations_queue = []
    for job_num in jobs:
        for op_idx, op_data in enumerate(jobs[job_num]):
            operations_queue.append((job_num, op_idx, op_data))

    while operations_queue:
        best_op = None
        best_machine = None
        min_end_time_estimation = float('inf')

        for job_num, op_idx, op_data in operations_queue:
            eligible_machines = op_data[0]
            processing_times = op_data[1]

            for i, machine in enumerate(eligible_machines):
                processing_time = processing_times[i]
                start_time = max(machine_availability[machine], job_completion_times[job_num])
                end_time_estimation = start_time + processing_time

                if end_time_estimation < min_end_time_estimation:
                    min_end_time_estimation = end_time_estimation
                    best_op = (job_num, op_idx, op_data)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

        job_num, op_idx, op_data = best_op

        schedule.setdefault(job_num, []).append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_availability[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_num] = best_start_time + best_processing_time

        operations_queue.remove(best_op)

    return schedule
