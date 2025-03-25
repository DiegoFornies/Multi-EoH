
def heuristic(input_data):
    """A heuristic for FJSSP that minimizes makespan by considering machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize machine load
    machine_load = {m: 0 for m in range(n_machines)}

    #Iterate through the jobs
    for job_id, operations in jobs.items():
        schedule[job_id] = []
        #Iterate through the operations
        for op_idx, operation in enumerate(operations):
            available_machines, processing_times = operation
            op_num = op_idx + 1

            # Evaluate machine selection based on load and availability
            best_machine = None
            min_end_time = float('inf')

            #Iterate through the available machines
            for m_idx, machine in enumerate(available_machines):
                processing_time = processing_times[m_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time
                # If the machine load is lower
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability time and job completion time
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
           

    return schedule
