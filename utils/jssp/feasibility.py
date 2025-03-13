def feasibility(instance, solution):
    def operation_feasibility():
        for job, operations in solution.items():
            job_operations = instance['jobs'][job]
            for op_idx, op in enumerate(operations):
                assigned_machine = int(op['Assigned Machine'])
                job_machine_list, job_processing_times = job_operations[op_idx]
                if assigned_machine not in job_machine_list:
                    return False
                assigned_processing_time = op['Processing Time']
                if assigned_processing_time != job_processing_times[job_machine_list.index(assigned_machine)]:
                    return False
        return True

    def machine_feasibility():
        machine_operations = {int(machine): [] for machine in range(1, instance['n_machines'] + 1)}
        for job, operations in solution.items():
            for op in operations:
                assigned_machine = int(op['Assigned Machine'])
                start_time = op['Start Time']
                end_time = op['End Time']
                machine_op_list = machine_operations[assigned_machine]

                for existing_op in machine_op_list:
                    if not (end_time <= existing_op['Start Time'] or start_time >= existing_op['End Time']):
                        return False
                
                machine_op_list.append({'Start Time': start_time, 'End Time': end_time})
                machine_operations[assigned_machine] = machine_op_list

        return True

    def sequence_feasibility():
        for job, operations in solution.items():
            for op_idx in range(1, len(operations)):
                prev_op_end_time = operations[op_idx - 1]['End Time']
                curr_op_start_time = operations[op_idx]['Start Time']
                if curr_op_start_time < prev_op_end_time:
                    return False
        return True
    print(solution)
    print(machine_feasibility(), operation_feasibility(), sequence_feasibility())
    return machine_feasibility() and operation_feasibility() and sequence_feasibility()
