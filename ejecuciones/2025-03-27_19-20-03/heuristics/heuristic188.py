
def heuristic(input_data):
    """Schedules jobs based on earliest finish time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx, machines, times))

    scheduled_operations = 0
    total_operations = len(operations)

    while scheduled_operations < total_operations:
        best_operation = None
        best_machine = None
        min_finish_time = float('inf')

        for job_id, op_idx, machines, times in operations:
            if job_id in schedule and len(schedule[job_id]) > op_idx and schedule[job_id][op_idx]['Assigned Machine'] is not None:
                continue
            
            if job_id not in schedule:
                continue
            
            if len(schedule[job_id]) <= op_idx:
                pass
            
            if len(schedule[job_id]) > 0 and op_idx > 0 and len(schedule[job_id]) != op_idx:
                continue
                
            if op_idx > 0 and len(schedule[job_id]) > 0 and schedule[job_id][op_idx-1]['End Time'] == None:
                continue
                

            available = True
            if op_idx > 0 and job_id in schedule and len(schedule[job_id]) > 0:
                if schedule[job_id][op_idx-1]['End Time'] == None:
                    available = False

            if not available:
                continue

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                finish_time = start_time + processing_time

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_operation = (job_id, op_idx, machines, times)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
                    
        if best_operation is None:
            break

        job_id, op_idx, machines, times = best_operation
        if job_id not in schedule:
            schedule[job_id] = []
        
        while len(schedule[job_id]) < op_idx:
            schedule[job_id].append({})

        if len(schedule[job_id]) == op_idx:
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time
        else:
            schedule[job_id][op_idx] = {
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            }
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time

        scheduled_operations += 1

    return schedule
