
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes machines with earlier availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_end_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, operation in enumerate(operations):
            machines, times = operation

            # Find the machine with the earliest available time among the possible machines
            best_machine = None
            min_available_time = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                available_time = machine_available_time[machine]
                
                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the best machine
            start_time = max(min_available_time, job_end_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_end_time[job_id] = end_time

    return schedule
