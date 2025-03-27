
def heuristic(input_data):
    """Prioritizes minimizing idle time while considering machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    operations_queue = []
    for job in range(1, n_jobs + 1):
        operations_queue.append((job, 0))  # (job, operation_index)

    while operations_queue:
        best_job, best_op_idx = None, None
        min_idle_time = float('inf')

        for job, op_idx in operations_queue:
            machines, times = jobs_data[job][op_idx]
            op_num = op_idx + 1

            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                idle_time = start_time - machine_available_time[machine]

                if idle_time < min_idle_time:
                    min_idle_time = idle_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
                    best_job = job
                    best_op_idx = op_idx

        operations_queue.remove((best_job, best_op_idx))
        machines, times = jobs_data[best_job][best_op_idx]
        op_num = best_op_idx + 1
        i = machines.index(best_machine)
        processing_time = times[i]
        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])
        end_time = start_time + processing_time

        schedule[best_job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[best_job] = end_time

        if best_op_idx + 1 < len(jobs_data[best_job]):
            operations_queue.append((best_job, best_op_idx + 1))

    return schedule
