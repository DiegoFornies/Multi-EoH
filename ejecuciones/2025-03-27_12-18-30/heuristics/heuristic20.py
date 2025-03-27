
def heuristic(input_data):
    """Schedules jobs using a shortest processing time and earliest machine availability heuristic."""
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}  # Track total processing time for each machine

    job_schedule = {}
    for job_id, operations in jobs_data.items():
        job_schedule[job_id] = []
        job_finish_time = 0

        for op_idx, operation in enumerate(operations):
            machines, times = operation

            # Find the machine with the shortest processing time for this operation AND earliest availability.
            best_machine, min_time = None, float('inf')
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                if processing_time < min_time:
                    min_time = processing_time
                    best_machine = machine
            
            start_time = max(machine_available_time[best_machine], job_finish_time) # Ensure both machine and job are available
            end_time = start_time + min_time

            job_schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': min_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += min_time
            job_finish_time = end_time #Update lastest job finish time.

    return job_schedule
