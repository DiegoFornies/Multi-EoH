
def heuristic(input_data):
    """Heuristic for FJSSP: SPT and random machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    import random

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Shortest Processing Time + Random Machine Selection
            min_time = float('inf')
            valid_machines = []

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                if processing_time < min_time:
                    min_time = processing_time
                    valid_machines = [machine]
                elif processing_time == min_time:
                    valid_machines.append(machine)

            best_machine = random.choice(valid_machines)
            processing_time = times[machines.index(best_machine)]  # Find the correct processing time
            start_time = max(machine_load[best_machine], job_completion_times[job])
            end_time = start_time + processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            machine_load[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
