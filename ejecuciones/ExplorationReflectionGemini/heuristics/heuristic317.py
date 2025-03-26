
def heuristic(input_data):
    """Schedules jobs using a combined machine load and job criticality heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Calculate job criticality based on remaining processing time
    job_criticality = {}
    for job_id in range(1, n_jobs + 1):
        remaining_time = sum(min(times) for machines, times in jobs[job_id])
        job_criticality[job_id] = remaining_time

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, machines, times))

    operations.sort(key=lambda x: (job_criticality[x[0]], x[0], x[1]))

    scheduled_ops = set()

    while len(scheduled_ops) < len(operations):
        eligible_operations = []
        for job_id, op_idx, machines, times in operations:
            if (job_id, op_idx) not in scheduled_ops:
                if op_idx == 0 or ((job_id, op_idx - 1) in scheduled_ops and job_completion_time[job_id] > 0):
                    eligible_operations.append((job_id, op_idx, machines, times))

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        best_start_time = float('inf')

        for job_id, op_idx, machines, times in eligible_operations:
            # Prioritize machines with lower load
            available_machines = []
            for idx, machine in enumerate(machines):
                available_machines.append((machine, times[idx]))
            
            best_available_time = float('inf')
            best_available_machine = None

            for m, t in available_machines:
                start_time = max(machine_time[m], job_completion_time[job_id])
                if start_time < best_available_time:
                    best_available_time = start_time
                    best_available_machine = m

            if best_available_time < best_start_time:
                best_start_time = best_available_time
                best_op = (job_id, op_idx, machines, times)
                best_machine = best_available_machine

        if best_op is not None:
            job_id, op_idx, machines, times = best_op
            op_num = op_idx + 1

            processing_time = times[machines.index(best_machine)]

            start_time = max(machine_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time[job_id] = end_time
            scheduled_ops.add((job_id, op_idx))

    return schedule
