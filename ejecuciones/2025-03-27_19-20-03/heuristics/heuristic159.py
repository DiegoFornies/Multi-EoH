
def heuristic(input_data):
    """Schedules jobs using shortest processing time and earliest start time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    remaining_operations = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
          schedule[job_id] = []

    all_ops = []
    for job_id in range(1, n_jobs+1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            machines, times = op_data
            all_ops.append((min(times), job_id, op_idx, machines, times)) # (min_time, job, op_idx, machines, times)
    
    all_ops.sort() # Sort the operations based on minimum processing time

    for _, job_id, op_idx, machines, times in all_ops:

        best_machine = None
        min_start_time = float('inf')
        best_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_time[job_id])
            
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time = times[m_idx]

        start_time = max(machine_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

        machine_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
    
    return schedule
