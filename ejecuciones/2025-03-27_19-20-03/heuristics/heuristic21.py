
def heuristic(input_data):
    """Heuristic for FJSSP: SPT-based dispatching with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    operation_queue = []

    # Initialize operation queue: (job, operation_index, processing_time)
    for job, ops in jobs.items():
        machines, times = ops[0]
        best_machine = machines[0]
        min_time = times[0]
        for i in range(len(machines)):
            if times[i] < min_time:
                min_time = times[i]
                best_machine = machines[i]
        operation_queue.append((job, 0, min_time, best_machine))  # Job, op index, SPT, preferred machine

    operation_queue.sort(key=lambda x: x[2])  # Sort by SPT

    machine_timeline = {m: [] for m in range(n_machines)}  # Keep track of machine availability

    current_time = 0
    completed_operations = {job: -1 for job in jobs}

    while operation_queue:
        job, op_idx, processing_time, preferred_machine = operation_queue.pop(0)
        
        machines, times = jobs[job][op_idx]

        # Find the best machine considering availability and processing time
        best_machine = -1
        min_completion_time = float('inf')
        chosen_processing_time = -1

        for i, machine in enumerate(machines):
            available_time = 0
            if machine_timeline[machine]:
                available_time = machine_timeline[machine][-1]['End Time']
            
            # Adjust the start time to consider the job's precedence constraint.
            job_available_time = 0
            if op_idx > 0:
                job_available_time = schedule[job][-1]['End Time']
            
            start_time = max(available_time, job_available_time)
            completion_time = start_time + times[i]
            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                chosen_processing_time = times[i]
                best_start_time = start_time

        
        if best_machine == -1:
            raise ValueError("No suitable machine found for operation.")

        start_time = best_start_time
        end_time = start_time + chosen_processing_time
            
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': chosen_processing_time
        })
        
        machine_timeline[best_machine].append({'Job': job, 'Operation': op_idx + 1, 'Start Time': start_time, 'End Time': end_time})
        machine_timeline[best_machine].sort(key=lambda x: x['Start Time'])
        
        completed_operations[job] = op_idx
        
        # Add the next operation to the queue if it exists
        if op_idx + 1 < len(jobs[job]):
            next_machines, next_times = jobs[job][op_idx + 1]
            best_next_machine = next_machines[0]
            min_next_time = next_times[0]
            for i in range(len(next_machines)):
                if next_times[i] < min_next_time:
                    min_next_time = next_times[i]
                    best_next_machine = next_machines[i]
            operation_queue.append((job, op_idx + 1, min_next_time, best_next_machine))
            operation_queue.sort(key=lambda x: x[2]) # Sort by SPT
    
    return schedule
