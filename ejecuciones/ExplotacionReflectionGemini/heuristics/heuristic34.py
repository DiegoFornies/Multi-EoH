
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes minimizing idle time on machines."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_assignments = {m: [] for m in range(n_machines)}  # Track assignments to calculate balance

    schedule = {}
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_job = jobs[job_id]
        current_job_time = 0
        
        for operation_index, operation in enumerate(current_job):
            feasible_machines, processing_times = operation
            best_machine, best_processing_time, best_start_time = None, None, float('inf')

            for machine_index, machine_id in enumerate(feasible_machines):
                processing_time = processing_times[machine_index]
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])
                # Prioritize machines that are available sooner to minimize idle time.
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine_id
                    best_processing_time = processing_time

            end_time = best_start_time + best_processing_time
            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time  # Update job completion time
            machine_assignments[best_machine].append((job_id, operation_index + 1)) #Track job and op assignment

    return schedule
