
def heuristic(input_data):
    """Schedules jobs using a Least Work Remaining (LWR) rule and machine load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_work = {}

    # Calculate total work remaining for each job.
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_remaining_work[job] = total_time

    # Create a list of (job, operation_index) tuples.
    job_queue = []
    for job in range(1, n_jobs + 1):
        job_queue.append((job, 0))

    while job_queue:
        # Sort jobs by remaining work, considering machine load.
        job_queue.sort(key=lambda x: (job_remaining_work[x[0]],sum(machine_load.values())/n_machines) )
        job, op_idx = job_queue.pop(0)

        if job not in schedule:
            schedule[job] = []

        machines, times = jobs_data[job][op_idx]
        op_num = op_idx + 1

        # Find the machine with the least load among feasible machines.
        best_machine, best_time, best_processing_time = None, float('inf'), None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < best_time:
                best_machine = machine
                best_time = start_time
                best_processing_time = times[m_idx]

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        processing_time = best_processing_time
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job data.
        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += processing_time
        job_completion_time[job] = end_time
        job_remaining_work[job] -= processing_time

        # Add the next operation of the job to the queue if it exists.
        if op_idx + 1 < len(jobs_data[job]):
            job_queue.append((job, op_idx + 1))

    return schedule
