
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations based on shortest processing time among available machines.
    Chooses the machine that allows for the earliest completion of the operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs_data[job_id]

        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1
            
            best_machine = None
            min_end_time = float('inf')
            processing_time = 0
            
            # Find best machine based on earliest completion time
            for i, machine in enumerate(machines):
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job_id])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[i]

            # Schedule operation on the best machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
