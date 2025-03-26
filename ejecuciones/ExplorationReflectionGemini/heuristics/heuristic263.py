
def heuristic(input_data):
    """Schedules jobs using SPT and least loaded machine, dynamically adjusting priority."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_combined_priority = float('inf')

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                
                # Dynamically adjust priority: SPT + Least Loaded
                priority = processing_time + 0.1 * machine_load[machine] #Weight the least loaded a bit less
                
                if priority < min_combined_priority:
                    min_combined_priority = priority
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            # Schedule operation to the best machine found
            start_time = best_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job states
            machine_available_times[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_times[job_id] = end_time

    return schedule
