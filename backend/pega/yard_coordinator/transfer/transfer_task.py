from backend.pega.yard_coordinator.transfer.transfer_from_workbasket_to_hostler import TransferFromWorkbasketToHostler


class TransferTask:
    """
    Transfers a task between workbasket and hostler (checker) in Pega.
    Determines transfer type based on assigned_to and target values:
      - hostler → hostler: both are not None and not equal (delete & create)
      - hostler → workbasket: assigned_to not None, target is None (delete & create)
      - workbasket → hostler: assigned_to is None, target not None (direct transfer)
    """

    def __init__(
            self,
            case_id,
            assigned_to,
            target,
            session_manager,
            **kwargs
    ):
        self.extra = kwargs
        self.case_id = case_id
        self.assigned_to = assigned_to
        self.target = target
        self.session_manager = session_manager

    async def transfer(self, redis):
        # 1. Get task data from Redis
        task_data = await self.session_manager.task_store.get_task(self.case_id)
        if not task_data:
            return {
                "success": False,
                "method": "lookup",
                "case_id": self.case_id,
                "assigned_to": self.assigned_to,
                "error": "Task not found"
            }

        # 2. Validate arguments
        if self.assigned_to == self.target:
            return {
                "success": False,
                "method": "validation",
                "case_id": self.case_id,
                "assigned_to": self.assigned_to,
                "error": "assigned_to and target must be different for a transfer."
            }

        # 3. Direct Transfer: workbasket → hostler
        if self.assigned_to is None and self.target:
            transfer = TransferFromWorkbasketToHostler(
                case_id=self.case_id,
                checker_id=self.target,
                session_manager=self.session_manager,
            )
            await transfer.transfer()
            return {
                "success": True,
                "method": "direct",
                "case_id": self.case_id,
                "assigned_to": self.target,
                "error": None
            }

        # 4. Delete & Create: hostler→hostler, hostler→workbasket
        if self.assigned_to and self.target:
            new_assigned_to = self.target
            method = "delete_create"
        elif self.assigned_to and self.target is None:
            new_assigned_to = "WORKBASKET"
            method = "delete_create"
        else:
            return {
                "success": False,
                "method": "validation",
                "case_id": self.case_id,
                "assigned_to": self.assigned_to,
                "error": "Invalid argument combination for transfer. Must provide assigned_to or target."
            }

        # Delete the original task
        await self.session_manager.run_delete_task(self.case_id)
        # Create new task with same data, new assignment
        created = await self.session_manager.run_create_task(
            yard_task_type=task_data.get("yard_task_type"),
            trailer_number=task_data.get("trailer"),
            door=task_data.get("door"),
            assigned_to=new_assigned_to,
            status="PENDING",
            locked=False,
            general_note=task_data.get("note") or "",
            priority=task_data.get("priority") or "Normal",
        )
        if not created:
            return {
                "success": False,
                "method": method,
                "case_id": self.case_id,
                "assigned_to": new_assigned_to,
                "error": "Failed to create new task"
            }
        return {
            "success": True,
            "method": method,
            "case_id": self.case_id,
            "assigned_to": new_assigned_to,
            "error": None
        }
