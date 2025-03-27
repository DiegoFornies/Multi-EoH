
def heuristic(input_data):
    """
    Schedules jobs using a shortest processing time (SPT) rule
    while considering machine workload balance.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}

    operations_list = []
    for job, operations in jobs_data.items():
        for op_idx, operation_data in enumerate(operations):
            operations_list.append((job, op_idx + 1))
    
    while operations_list:
        best_op = None
        best_machine = None
        min_end_time = float('inf')
        
        for job, op_num in operations_list:
            machines, times = jobs_data[job][op_num - 1]
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = max(machine_available_times[machine], job_completion_times[job])
                end_time = available_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job, op_num)
                    best_machine = machine
        
        job, op_num = best_op
        machines, times = jobs_data[job][op_num - 1]
        m_idx = machines.index(best_machine)
        processing_time = times[m_idx]
        start_time = max(machine_available_times[best_machine], job_completion_times[job])
        end_time = start_time + processing_time

        scheduled_operations[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_times[best_machine] = end_time
        machine_load[best_machine] += processing_time
        job_completion_times[job] = end_time
        
        operations_list.remove((job, op_num))
        
    return scheduled_operations
