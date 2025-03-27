
def heuristic(input_data):
    """Combines shortest processing time and least loaded machine for FJSSP."""
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    n_jobs = input_data['n_jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs+1)}
    schedule = {}

    remaining_operations = {job: [i for i in range(len(ops))] for job, ops in jobs_data.items()}

    available_operations = []
    for job in jobs_data:
        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))
    
    while available_operations:
        best_op = None
        min_makespan = float('inf')

        for job, op_idx in available_operations:
            machines, processing_times = jobs_data[job][op_idx]
            
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                makespan = start_time + processing_times[m_idx] + machine_load[m] 
                if makespan < min_makespan:
                    min_makespan = makespan
                    best_machine = m
                    best_processing_time = processing_times[m_idx]
                    min_start_time = start_time

            if best_machine is not None:
                start_time = max(machine_available_times[best_machine], job_completion_times[job])
                
                if start_time < min_makespan:
                    min_makespan = start_time
                    best_op = (job, op_idx, best_machine, best_processing_time, start_time)

        if best_op is not None:
            job, op_idx, assigned_machine, processing_time, start_time = best_op
            end_time = start_time + processing_time

            if job not in schedule:
                schedule[job] = []
            
            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            
            remaining_operations[job].pop(0)

            machine_load[assigned_machine] += processing_time
            machine_available_times[assigned_machine] = end_time
            job_completion_times[job] = end_time
            
            if remaining_operations[job]:
                available_operations.append((job, remaining_operations[job][0]))

            available_operations.remove((job, op_idx))

    return schedule
