
def heuristic(input_data):
    """Schedules jobs using a shortest processing time and earliest due date strategy."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_due_date = {}
    for job in jobs:
        total_time = 0
        for machines, times in jobs[job]:
            total_time+=min(times)
        job_due_date[job]= total_time
    
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    def calculate_priority(job, op_idx,time):
        return time

    while operations:
        best_op = None
        best_priority = float('inf')
        for i in range(len(operations)):
          job, op_idx, machines, times = operations[i]
          min_time = min(times)
          priority = calculate_priority(job,op_idx,min_time)
          if priority < best_priority:
            best_priority = priority
            best_op = i

        job, op_idx, machines, times = operations.pop(best_op)
        
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx in range(len(machines)):
          m = machines[m_idx]
          t = times[m_idx]
          start_time = machine_available_time[m]
          
          if start_time < best_start_time:
            best_start_time = start_time
            best_machine = m
            best_processing_time = t
            
        start_time = max(best_start_time, sum(op['Processing Time'] for op in schedule[job]))
        end_time = start_time + best_processing_time
        operation_number = op_idx+1
        
        schedule[job].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = end_time
    return schedule
