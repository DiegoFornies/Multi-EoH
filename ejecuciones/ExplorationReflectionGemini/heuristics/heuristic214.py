
def heuristic(input_data):
    """Prioritizes operations with the fewest possible machines."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Prioritize operations with the fewest machine choices
            best_machine = None
            best_processing_time = None
            start_time = None

            #First, find the machine with shortest wait time
            min_wait_time = float('inf')
            selected_machine = None
            selected_processing_time = None

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                
                current_start_time = max(machine_available_times[machine], job_completion_times[job_id])
                wait_time = current_start_time - machine_available_times[machine]
                if wait_time < min_wait_time:
                    min_wait_time = wait_time
                    selected_machine = machine
                    selected_processing_time = processing_time

            best_machine = selected_machine
            best_processing_time = selected_processing_time

            # Schedule operation to the best machine found
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
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
            job_completion_times[job_id] = end_time

    return schedule
