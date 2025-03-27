
def heuristic(input_data):
    """Schedules jobs by iterative machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Initial assignment: assign each operation to the first available machine
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            machine = machines[0]
            time = times[0]
            start_time = max(machine_time[machine], job_completion_time[job])
            end_time = start_time + time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': time
            })

            machine_time[machine] = end_time
            job_completion_time[job] = end_time

    # Iterative improvement: try to move operations to less loaded machines
    for _ in range(5):  # Iterate a few times for improvement
        for job in range(1, n_jobs + 1):
            for op_idx in range(len(jobs[job])):
                original_machine = schedule[job][op_idx]['Assigned Machine']
                original_start_time = schedule[job][op_idx]['Start Time']
                original_end_time = schedule[job][op_idx]['End Time']
                original_processing_time = schedule[job][op_idx]['Processing Time']

                machines, times = jobs[job][op_idx]
                best_machine = original_machine
                best_start_time = original_start_time
                best_end_time = original_end_time
                best_processing_time = original_processing_time

                # Try all alternative machines
                for m_idx, machine in enumerate(machines):
                    if machine != original_machine:
                        time = times[m_idx]
                        start_time = max(machine_time[machine],
                                         job_completion_time[job] if op_idx == 0 else schedule[job][op_idx-1]['End Time'])
                        end_time = start_time + time

                        # Calculate the change in makespan if this move is made

                        if end_time < best_end_time:
                            best_machine = machine
                            best_start_time = start_time
                            best_end_time = end_time
                            best_processing_time = time

                # If a better machine is found, update the schedule
                if best_machine != original_machine:

                    # update start/end for the current operation in schedule
                    schedule[job][op_idx]['Assigned Machine'] = best_machine
                    schedule[job][op_idx]['Start Time'] = best_start_time
                    schedule[job][op_idx]['End Time'] = best_end_time
                    schedule[job][op_idx]['Processing Time'] = best_processing_time

                    # reset job completion and machine time and recalculate these values from the beginning
                    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                    machine_time = {m: 0 for m in range(n_machines)}

                    for j in range(1, n_jobs + 1):
                        current_time = 0
                        for op_idx2 in range(len(jobs[j])):
                            assigned_machine = schedule[j][op_idx2]['Assigned Machine']
                            start_time = max(machine_time[assigned_machine],
                                             job_completion_time[j] if op_idx2 == 0 else schedule[j][op_idx2-1]['End Time'])
                            end_time = start_time + schedule[j][op_idx2]['Processing Time']
                            schedule[j][op_idx2]['Start Time'] = start_time
                            schedule[j][op_idx2]['End Time'] = end_time
                            machine_time[assigned_machine] = end_time
                            job_completion_time[j] = end_time

    return schedule
