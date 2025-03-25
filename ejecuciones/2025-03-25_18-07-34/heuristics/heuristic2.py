
def heuristic(input_data):
    """
    A heuristic for the FJSSP that considers machine load and operation order.
    Prioritizes machines with less load when assigning operations.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Completion time of each job
    
    #Initialize schedule for each Job.
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    for job_id, operations in jobs.items():
        current_job_time = 0
        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1

            #Find the best machine based on current load and availabilty
            best_machine = None
            min_end_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_load[machine], current_job_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
                
            #Assign operations to the selected machine.
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            #Update load and job status
            machine_load[best_machine] = best_start_time + best_processing_time
            current_job_time = best_start_time + best_processing_time
            job_completion_times[job_id] = current_job_time

    return schedule
