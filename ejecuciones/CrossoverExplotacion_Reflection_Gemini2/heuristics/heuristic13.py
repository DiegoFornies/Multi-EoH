
def heuristic(input_data):
    """
    Heuristic for FJSSP: Chooses the machine with the earliest available time 
    among feasible machines for each operation to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        for operation_id, (machines, times) in enumerate(operations):
            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
            
            machine_available_time[best_machine] = min_end_time
            job_completion_time[job_id] = min_end_time
            
            schedule[job_id].append({
                'Operation': operation_id + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

    return schedule
