
def heuristic(input_data):
    """Heuristic for FJSSP: Balances makespan, separation, and machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine, best_processing_time = None, None
        earliest_completion_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]
            
            possible_machines = []
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                completion_time = start_time + processing_time
                possible_machines.append((machine_id, processing_time, start_time, completion_time))
            
            #Prioritize machines based on completion time, with a bias to balance machine load
            possible_machines.sort(key=lambda x: (x[3], machine_available_times[x[0]]))
            
            machine_id, processing_time, start_time, completion_time = possible_machines[0]
            
            if completion_time < earliest_completion_time:
                earliest_completion_time = completion_time
                best_job, best_op_index = job_id, op_index
                best_machine, best_processing_time = machine_id, processing_time
                best_start_time = start_time


        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[best_job] = best_start_time + best_processing_time
        
        schedule[best_job].append({
            'Operation': best_op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((best_job, best_op_index))

        if best_op_index + 1 < len(jobs_data[best_job]):
            ready_operations.append((best_job, best_op_index + 1))

    return schedule
