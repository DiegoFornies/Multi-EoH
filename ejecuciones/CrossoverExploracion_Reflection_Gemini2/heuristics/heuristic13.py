
def heuristic(input_data):
    """
    Heuristic for FJSSP scheduling. Prioritizes jobs based on remaining processing time.
    Chooses the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data.keys()}
    remaining_processing_time = {}

    # Calculate initial remaining processing time for each job
    for job, operations in jobs_data.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)  # Use the shortest processing time if there are choices
        remaining_processing_time[job] = total_time

    # Sort jobs based on remaining processing time (shortest first)
    job_priority = sorted(jobs_data.keys(), key=lambda job: remaining_processing_time[job])

    for job in job_priority:
        schedule[job] = []
        current_time = job_completion_time[job]
        
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time among the feasible machines
            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], current_time)
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[i]

            if best_machine is None:
                # Handle case where no machine is available (should not happen with proper input)
                print(f"Error: No available machine for job {job}, operation {op_num}")
                return None

            start_time = max(machine_available_time[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
