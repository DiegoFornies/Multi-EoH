
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT, earliest start, and load balancing."""
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
            min_score = float('inf')
            best_processing_time = None
            best_start_time = None

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time
                # Combine earliest start and machine load.
                score = start_time + machine_load[machine]  # Favor early start and less loaded machines

                if score < min_score:
                    min_score = score
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time
                    best_end_time = end_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            machine_available[best_machine] = best_end_time
            job_completion[job_id] = best_end_time
            machine_load[best_machine] += best_processing_time

    return schedule
