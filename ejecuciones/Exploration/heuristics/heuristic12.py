
def heuristic(input_data):
    """
    A heuristic algorithm for the Flexible Job Shop Scheduling Problem (FJSSP)
    Prioritizes minimizing makespan by selecting machines with the earliest
    available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs_data[job_id]

        for op_idx, operation in enumerate(operations):
            machines, times = operation

            # Find the machine with the earliest available time among feasible machines.
            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[i]

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time
            
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times.
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
