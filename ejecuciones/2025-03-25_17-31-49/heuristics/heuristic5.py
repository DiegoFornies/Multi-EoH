
def heuristic(input_data):
    """A heuristic for FJSSP that minimizes makespan and balances load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize data structures
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_loads = {m: 0 for m in range(n_machines)}
    schedule = {}

    # Iterate through jobs, prioritizing jobs with more operations
    job_order = sorted(jobs.keys(), key=lambda job_id: len(jobs[job_id]), reverse=True)

    for job_id in job_order:
        schedule[job_id] = []
        operations = jobs[job_id]
        current_time = job_completion_times[job_id]

        for op_idx, op_data in enumerate(operations):
            machines, times = op_data
            op_num = op_idx + 1

            # Find the machine with the earliest available time and lowest load
            best_machine, best_time = None, float('inf')
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                available_time = max(machine_available_times[machine], current_time)
                if available_time + processing_time < best_time:
                    best_time = available_time + processing_time
                    best_machine = machine
            
            # Schedule the operation on the selected machine
            start_time = max(machine_available_times[best_machine], current_time)
            processing_time = times[machines.index(best_machine)]
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine availability and job completion time
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            machine_loads[best_machine] += processing_time

    return schedule
