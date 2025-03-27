
def heuristic(input_data):
    """Schedules jobs, prioritizing shortest processing time on least loaded machine."""
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {}

    for job_id, operations in jobs_data.items():
        schedule[job_id] = []
        for op_idx, op_data in enumerate(operations):
            machines, processing_times = op_data
            op_num = op_idx + 1

            # Prioritize machines with the shortest processing time and least load.
            best_machine = None
            min_makespan = float('inf')

            for machine_idx, machine in enumerate(machines):
                start_time = max(machine_load[machine], job_completion_times[job_id])
                makespan = start_time + processing_times[machine_idx]
                if makespan < min_makespan:
                    min_makespan = makespan
                    best_machine = machine
                    best_processing_time = processing_times[machine_idx]
            
            start_time = max(machine_load[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time
                    
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            machine_load[best_machine] = end_time
            job_completion_times[job_id] = end_time
    return schedule
