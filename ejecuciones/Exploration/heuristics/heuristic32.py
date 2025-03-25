
def heuristic(input_data):
    """
    Implements a heuristic for the Flexible Job Shop Scheduling Problem (FJSSP)
    using a shortest processing time (SPT) and earliest available machine strategy.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times
    
    for job_id in jobs:
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, operation in enumerate(operations):
            machines, processing_times = operation
            op_num = op_idx + 1

            # Find the machine with the earliest available time among the feasible machines.
            best_machine = None
            min_available_time = float('inf')
            best_processing_time = float('inf')

            for i, machine in enumerate(machines):
                available_time = machine_available_times[machine]
                processing_time = processing_times[i]
                
                #Consider job sequencing constraints.
                start_time = max(available_time, job_completion_times[job_id])

                if start_time < min_available_time or (start_time == min_available_time and processing_time < best_processing_time): #tie breaker by shortest processing time
                    min_available_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            processing_time = processing_times[machines.index(best_machine)]
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
