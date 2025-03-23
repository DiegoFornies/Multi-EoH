
def heuristic(input_data):
    """Schedules jobs considering machine load and SPT for minimizing makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs_data[job_id]):
            machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_end_time = float('inf')
            min_processing_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time
                load_penalty = machine_load[machine] * 0.001  # Small penalty based on load

                if end_time + load_penalty < min_end_time:
                    min_end_time = end_time + load_penalty
                    best_machine = machine
                    min_processing_time = processing_time
                elif end_time + load_penalty == min_end_time and processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine

            start_time = max(machine_available[best_machine], job_completion[job_id])
            end_time = start_time + min_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': min_processing_time
            })

            machine_available[best_machine] = end_time
            job_completion[job_id] = end_time
            machine_load[best_machine] += min_processing_time

    return schedule
