
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes minimizing idle time and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        job_operations = jobs[job_id]
        job_start_time = 0  # Track the earliest start time for operations in this job

        for op_index, op_data in enumerate(job_operations):
            machines, processing_times = op_data
            op_number = op_index + 1

            # Find the best machine for this operation based on availability and load.
            best_machine = None
            min_end_time = float('inf')
            
            for m_index, machine in enumerate(machines):
                processing_time = processing_times[m_index]
                start_time = max(machine_available_time[machine], job_start_time) # ensure sequence feasibility constraint
                end_time = start_time + processing_time

                # Heuristic: Prioritize minimizing idle time and balancing load.
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time


            # Schedule the operation on the best machine.
            schedule[job_id].append({
                'Operation': op_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job start time for sequence feasibility.
            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_start_time = best_start_time + best_processing_time

    return schedule
