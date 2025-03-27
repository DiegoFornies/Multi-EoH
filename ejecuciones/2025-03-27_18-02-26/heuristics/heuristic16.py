
def heuristic(input_data):
    """
    A heuristic for FJSSP that considers machine load and job completion time to minimize makespan.
    It iterates through operations, assigns them to the least loaded feasible machine, and updates schedules.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_schedule = {m: [] for m in range(n_machines)}  # Keep track of scheduled intervals on each machine
    job_schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            best_machine = None
            min_start_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                available_time = machine_load[machine]
                start_time = max(available_time, job_completion_time[job])

                # Check for overlaps with existing schedule on the machine
                overlap = False
                for start, end in machine_schedule[machine]:
                    if not (start_time >= end or start_time + processing_time <= start):
                        overlap = True
                        break

                if not overlap and start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            if best_machine is not None:
                start_time = min_start_time
                end_time = start_time + best_processing_time
                job_schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine,
                                        'Start Time': start_time, 'End Time': end_time,
                                        'Processing Time': best_processing_time})

                machine_load[best_machine] = end_time
                job_completion_time[job] = end_time
                machine_schedule[best_machine].append((start_time, end_time))
            else:
                print(f"No suitable machine found for job {job}, operation {op_num}")

    return job_schedule
