
def heuristic(input_data):
    """A scheduling heuristic minimizing makespan by prioritizing operations with shortest processing time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Flatten operations into a list with job and operation info
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })
    
    # Sort operations based on shortest processing time
    operations.sort(key=lambda op: min(op['times']))
    
    scheduled_operations = 0
    while scheduled_operations < sum(len(ops) for ops in jobs_data.values()):
        for operation in operations:
            job_id = operation['job_id']
            op_idx = operation['op_idx']
            machines = operation['machines']
            times = operation['times']

            if job_id in schedule and len(schedule[job_id]) > op_idx:
                continue

            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None
            
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                    
            if best_machine is not None:
                end_time = best_start_time + best_processing_time

                if job_id not in schedule:
                    schedule[job_id] = []

                schedule[job_id].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': best_start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })
                    
                machine_available_time[best_machine] = end_time
                job_completion_time[job_id] = end_time
                scheduled_operations += 1

    return schedule
