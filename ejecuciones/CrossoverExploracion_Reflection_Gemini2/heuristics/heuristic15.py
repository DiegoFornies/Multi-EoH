
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that prioritizes
    minimizing idle time and balancing machine load using a greedy approach.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs based on the number of operations (shortest job first)
    job_order = sorted(jobs.keys(), key=lambda j: len(jobs[j]))

    for job in job_order:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine, best_start_time, best_processing_time = None, float('inf'), None

            # Iterate through feasible machines and times for the operation
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                # Calculate the earliest possible start time considering machine availability and job completion
                start_time = max(machine_available_times[machine], job_completion_times[job])

                # Evaluate the start time based on a weighted criteria
                # Criteria: Minimize Start Time(reduce makespan), Minimise Machine Idle Time.
                if start_time < best_start_time:
                    best_machine, best_start_time, best_processing_time = machine, start_time, processing_time

            # Assign the operation to the best machine
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job] = best_start_time + best_processing_time

    return schedule
