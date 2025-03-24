
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine load and operation processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation in enumerate(job_operations):
            machines, processing_times = operation
            op_num = operation_index + 1

            # Choose the machine with the earliest available time among feasible machines.
            best_machine = None
            min_available_time = float('inf')

            for m, time in zip(machines, processing_times):
                available_time = max(machine_available_time[m], job_completion_time[job_id])
                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = m
                    best_time = time

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += best_time # Track machine load
    return schedule
