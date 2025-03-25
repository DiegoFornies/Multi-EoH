
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine load and job completion time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs based on the number of operations
    sorted_jobs = sorted(jobs.items(), key=lambda item: len(item[1]))

    for job_id, operations in sorted_jobs:
        schedule[job_id] = []
        for op_idx, (machines, times) in enumerate(operations):
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_available_time = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                available_time = max(machine_available_time[machine], job_completion_time[job_id])

                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
