
def heuristic(input_data):
    """
    A heuristic for FJSSP that minimizes makespan and balances machine load.
    It assigns operations to the least loaded machine among feasible options.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_schedules = {m: [] for m in range(n_machines)} # Keep track of operation on machines

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        job_operations = jobs_data[job]

        for op_idx, operation in enumerate(job_operations):
            machines, times = operation
            
            # Find the least loaded machine among feasible options
            best_machine = None
            min_load = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]

                # Calculate potential start time considering machine availability and job sequence
                start_time = max(machine_load[machine], job_completion_times[job])
                
                # Check for overlaps with existing operations on the machine
                overlap = False
                for scheduled_op in machine_schedules[machine]:
                    if start_time < scheduled_op['End Time'] and (start_time + processing_time) > scheduled_op['Start Time']:
                        overlap = True
                        break

                if not overlap:
                    potential_load = start_time + processing_time
                    if potential_load < min_load:
                        min_load = potential_load
                        best_machine = machine
                        best_start_time = start_time
                        best_processing_time = processing_time

            # Assign operation to the best machine if one is found
            if best_machine is not None:
                schedule[job].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': best_start_time,
                    'End Time': best_start_time + best_processing_time,
                    'Processing Time': best_processing_time
                })
                
                machine_schedules[best_machine].append({
                    'Job': job,
                    'Operation': op_idx + 1,
                    'Start Time': best_start_time,
                    'End Time': best_start_time + best_processing_time,
                    'Processing Time': best_processing_time
                })

                machine_load[best_machine] = best_start_time + best_processing_time
                job_completion_times[job] = best_start_time + best_processing_time

            else:
                # Handle the case where no feasible machine is found (should not happen with valid input)
                print(f"Warning: No feasible machine found for Job {job}, Operation {op_idx + 1}")
                # Assign to first machine and time, but ensure no overlap
                m_idx = 0
                machine = machines[m_idx]
                processing_time = times[m_idx]
                
                # Find the earliest possible start time without overlap
                start_time = max(machine_load[machine], job_completion_times[job])
                
                while True:
                    overlap = False
                    for scheduled_op in machine_schedules[machine]:
                        if start_time < scheduled_op['End Time'] and (start_time + processing_time) > scheduled_op['Start Time']:
                            start_time = scheduled_op['End Time'] # Try the next available time slot
                            overlap = True
                            break
                    if not overlap:
                        break

                schedule[job].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': machine,
                    'Start Time': start_time,
                    'End Time': start_time + processing_time,
                    'Processing Time': processing_time
                })
                
                machine_schedules[machine].append({
                    'Job': job,
                    'Operation': op_idx + 1,
                    'Start Time': start_time,
                    'End Time': start_time + processing_time,
                    'Processing Time': processing_time
                })
                machine_load[machine] = start_time + processing_time
                job_completion_times[job] = start_time + processing_time
    return schedule
