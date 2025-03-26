
def heuristic(input_data):
    """Combines SPT and machine load balancing adaptively."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        eligible_operations = []
        for job in jobs:
            op_index = job_operations_scheduled[job]
            if op_index < len(jobs[job]):
                eligible_operations.append((job, op_index))

        if not eligible_operations:
            break

        best_job = None
        best_op_index = None
        best_machine = None
        min_end_time = float('inf')

        for job, op_index in eligible_operations:
            machines, times = jobs[job][op_index]

            for i, machine in enumerate(machines):
                start_time = max(machine_load[machine], job_completion_times[job])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_job = job
                    best_op_index = op_index
                    best_machine = machine
                    processing_time = times[i]
                    start_t = start_time

        if best_job is not None:
            op_num = best_op_index + 1
            end_time = start_t + processing_time

            schedule[best_job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_t,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_load[best_machine] = end_time
            job_completion_times[best_job] = end_time
            job_operations_scheduled[best_job] += 1

    return schedule
