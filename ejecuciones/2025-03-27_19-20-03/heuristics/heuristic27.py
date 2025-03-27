
def heuristic(input_data):
    """Heuristic scheduling for FJSSP to minimize makespan and balance machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    for job in jobs:
        schedule[job] = []

    # Iterate through operations of all jobs
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on shortest processing time on the fastest machine (SPT-FM)
    operations.sort(key=lambda x: min(x[3])) #using lambda for readability

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1 #Corrected operation number

        # Find the best machine for the current operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx, m in enumerate(machines):
            available_time = machine_available_time[m]
            processing_time = times[m_idx]
            start_time = max(available_time, job_completion_time[job]) #ensure job sequentiality

            if start_time < best_start_time:
                best_machine = m
                best_start_time = start_time
                best_processing_time = processing_time
        
        #schedule operation on the selected machine
        start_time = best_start_time
        end_time = start_time + best_processing_time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        machine_load[best_machine] += best_processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
    return schedule
