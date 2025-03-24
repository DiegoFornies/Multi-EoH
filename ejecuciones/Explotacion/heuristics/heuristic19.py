
def heuristic(input_data):
    """Combines min-workload machine with shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {machine: 0 for machine in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    eligible_operations = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_operations < total_operations:
        best_job = None
        best_machine = None
        best_op_idx = None
        start_time_min = float('inf')
        processing_time_min = float('inf')

        for job in range(1, n_jobs + 1):
            op_idx = eligible_operations[job]
            if op_idx < len(jobs[job]):
                machines, times = jobs[job][op_idx]

                for i, machine in enumerate(machines):
                    start_time = max(machine_load[machine], job_completion_times[job])
                    processing_time = times[i]

                    if start_time < start_time_min or (start_time == start_time_min and processing_time < processing_time_min):
                        start_time_min = start_time
                        processing_time_min = processing_time
                        best_job = job
                        best_machine = machine
                        best_op_idx = op_idx

        if best_job is not None:
            machines, times = jobs[best_job][best_op_idx]
            processing_time = None

            for i, machine_option in enumerate(jobs[best_job][best_op_idx][0]):
                if machine_option == best_machine:
                    processing_time = jobs[best_job][best_op_idx][1][i]
                    break
            
            start_time = max(machine_load[best_machine], job_completion_times[best_job])
            end_time = start_time + processing_time

            schedule[best_job].append({
                'Operation': best_op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_load[best_machine] = end_time
            job_completion_times[best_job] = end_time
            eligible_operations[best_job] += 1
            scheduled_operations += 1

    return schedule
