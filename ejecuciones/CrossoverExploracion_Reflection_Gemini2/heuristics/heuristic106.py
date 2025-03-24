
def heuristic(input_data):
    """Combines SPT, least loaded machine, and job priority."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_remaining_operations = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, processing_times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            # Prioritize machines with less load
            available_machines = []
            for i, machine in enumerate(machines):
                 available_machines.append((machine, processing_times[i]))

            # find the machine that provides the earliest end time
            for machine, time in available_machines:
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = time

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += processing_time
            job_remaining_operations[job_id] -= 1
            

    return schedule
