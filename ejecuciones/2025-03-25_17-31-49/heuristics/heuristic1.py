
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes operations with the shortest processing time 
    and earliest machine availability to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    eligible_operations = []
    for job_id, operations in jobs_data.items():
        eligible_operations.append((job_id, 0)) # (job_id, operation_index)

    scheduled_operations = set()

    while eligible_operations:
        # Prioritize operations with smallest processing time, and earliest possible start
        best_op, best_machine, best_start_time, best_processing_time = None, None, float('inf'), float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]

            for machine_index, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                processing_time = times[machine_index]
                
                if processing_time < best_processing_time or (processing_time == best_processing_time and start_time < best_start_time):
                    best_op = (job_id, op_index)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job_id, op_index = best_op
        machines, times = jobs_data[job_id][op_index]
        machine_index = machines.index(best_machine)

        start_time = best_start_time
        processing_time = times[machine_index]
        end_time = start_time + processing_time

        # Update machine availability and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Update the schedule
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        eligible_operations.remove((job_id, op_index))

        # Add next operation for the job to the eligible operations list
        if op_index + 1 < len(jobs_data[job_id]):
            eligible_operations.append((job_id, op_index + 1))

    return schedule
