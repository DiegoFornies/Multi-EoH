
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time by scheduling operations
    on the machine that becomes available earliest. Also tries to balance machine workload.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}

    for job_id in jobs_data:
        schedule[job_id] = []

    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx, op_data))

    # Prioritize operations from jobs with the fewest remaining operations to be processed
    operations.sort(key=lambda x: len(jobs_data[x[0]]) - x[1])

    while operations:
        best_op = None
        best_machine = None
        earliest_start = float('inf')

        for job_id, op_idx, op_data in operations:
            machines, times = op_data

            # Ensure sequence feasibility
            if op_idx > 0 and job_completion_time[job_id] == 0: #first operation of a job has no prior operation
                continue

            if op_idx > 0:
                prev_op_end_time = schedule[job_id][op_idx - 1]['End Time']
            else:
                 prev_op_end_time = 0

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], prev_op_end_time)

                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = (job_id, op_idx, op_data)
                    best_machine = machine
                    best_processing_time = processing_time


        if best_op is not None:
            job_id, op_idx, op_data = best_op
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job_id] = end_time
            operations.remove(best_op)

    return schedule
