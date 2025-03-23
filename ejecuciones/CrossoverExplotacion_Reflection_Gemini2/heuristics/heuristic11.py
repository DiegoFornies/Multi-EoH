
def heuristic(input_data):
    """Heuristic for FJSSP: Sort jobs by number of operations, then uses earliest available time on best machine for each operation"""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Sort jobs by number of operations (shortest job first)
    job_order = sorted(jobs_data.keys(), key=lambda job: len(jobs_data[job]))

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data.keys()}
    schedule = {}

    for job in job_order:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            op_num = op_idx + 1
            
            # Find the earliest available time slot on the eligible machines.
            best_machine, min_start_time = None, float('inf')
            for i, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    processing_time = times[i]

            # Schedule the operation on the best machine at the earliest available time.
            start_time = min_start_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times.
            machine_available_times[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
