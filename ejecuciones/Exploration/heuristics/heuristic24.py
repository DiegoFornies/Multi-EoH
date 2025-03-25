
def heuristic(input_data):
    """A heuristic to schedule jobs minimizing makespan, idle time, and balancing machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}

    # Sort jobs by number of operations (shortest job first).
    sorted_jobs = sorted(jobs.items(), key=lambda item: len(item[1]))

    for job_id, operations in sorted_jobs:
        schedule[job_id] = []
        for op_idx, (machines, times) in enumerate(operations):
            op_num = op_idx + 1

            # Find the best machine for the current operation.  Prioritize machine available time and machine load.
            best_machine, best_time = None, float('inf')
            for i, m in enumerate(machines):
                available_time = max(machine_available_times[m], job_completion_times[job_id])
                if available_time + times[i] < best_time:
                    best_time = available_time + times[i]
                    best_machine = m
                    best_processing_time = times[i]

            # Schedule the operation on the best machine.
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine available time, job completion time, and machine load.
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            machine_load[best_machine] += best_processing_time

    return schedule
