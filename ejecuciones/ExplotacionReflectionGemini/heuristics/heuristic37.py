
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that
    prioritizes minimizing makespan and balancing machine load.
    It selects the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize data structures
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {}

    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        for op_idx, op_data in enumerate(operations):
            machines = op_data[0]
            processing_times = op_data[1]

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_available_time = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = processing_times[i]
                available_time = max(machine_available_time[machine], job_completion_time[job_id])

                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the best machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
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
            job_completion_time[job_id] = end_time

    return schedule
