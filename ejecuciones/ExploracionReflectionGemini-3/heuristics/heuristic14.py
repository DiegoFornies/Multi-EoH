
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time and balancing machine load.
    It schedules operations on machines with the earliest available time, considering machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)} # Keep track of current machine load

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]
        job_completion_time = 0 # Keep track of current job time

        for operation_index, operation in enumerate(job_operations):
            machines, processing_times = operation

            # Find the best machine for this operation
            best_machine = None
            min_start_time = float('inf')

            for m_index, machine in enumerate(machines):
                processing_time = processing_times[m_index]

                # Calculate the start time for this machine and operation
                start_time = max(machine_available_time[machine], job_completion_time)

                # If this start time is better than the current best, update the best machine
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine

            # Schedule the operation on the best machine
            processing_time = processing_times[machines.index(best_machine)]
            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job times
            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time = end_time

    return schedule
