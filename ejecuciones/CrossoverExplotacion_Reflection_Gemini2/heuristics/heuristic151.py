
def heuristic(input_data):
    """Combines SPT, earliest finish time, and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs_data[job_id]):
            machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_end_time = float('inf')
            min_processing_time = float('inf')
            min_machine_load = float('inf')

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time
                machine_load = machine_available[machine]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    min_machine_load = machine_load

                elif end_time == min_end_time:
                    if processing_time < min_processing_time:
                        min_processing_time = processing_time
                        best_machine = machine
                        best_processing_time = processing_time
                        min_machine_load = machine_load
                    elif processing_time == min_processing_time and machine_load < min_machine_load:
                        best_machine = machine
                        best_processing_time = processing_time
                        min_machine_load = machine_load
            
            start_time = max(machine_available[best_machine], job_completion[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available[best_machine] = end_time
            job_completion[job_id] = end_time

    return schedule
