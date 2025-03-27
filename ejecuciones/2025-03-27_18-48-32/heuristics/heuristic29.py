
def heuristic(input_data):
    """A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP)."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine availability times.
    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)} # Keep track of machine workload for balancing

    # Prioritize jobs based on total processing time to start shortest jobs earlier.
    job_priorities = {}
    for job, operations in jobs.items():
        total_time = sum(min(times) for _, times in operations) # Use min time if flexible
        job_priorities[job] = total_time

    sorted_jobs = sorted(job_priorities.items(), key=lambda item: item[1])

    for job_item in sorted_jobs:
        job = job_item[0]
        schedule[job], job_time = [], 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Find the best machine with the earliest available time and shortest processing time for this operation.
            best_machine = None
            min_end_time = float('inf')

            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], job_time)
                end_time = start_time + times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = m
                    best_time = times[m_idx]
            
            if best_machine is None:
                #Handle the edge case where somehow no machines were selected (shouldnt happen, but safe coding)
                best_machine = machines[0] # Fallback to the first machine
                best_time = times[0]

            # Assign the operation to the best machine.
            start = max(machine_time[best_machine], job_time)
            end = start + best_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start,
                'End Time': end,
                'Processing Time': best_time
            })

            # Update machine and job times.
            machine_time[best_machine] = end
            machine_load[best_machine] += best_time
            job_time = end

    return schedule
