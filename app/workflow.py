from enum import Enum
from pydantic import BaseModel


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowStep(BaseModel):
    name: str
    status: StepStatus = StepStatus.PENDING
    error: str | None = None

class PaymentWorkflow(BaseModel):
    customer_id: str
    payment_id: str
    amount: float
    steps: list[WorkflowStep] = [
        WorkflowStep(name="retrieve_customer"),
        WorkflowStep(name="check_balance"),
        WorkflowStep(name="record_payment"),
        WorkflowStep(name="verify_balance")
    ]

    def update_step(
        self,
        step_name: str,
        status: StepStatus,
        error: str | None = None,
    ) -> None:
        for step in self.steps:
            if step.name == step_name:
                step.status = status
                step.error = error
                return

        raise ValueError(f"Unknown workflow step: {step_name}")

    
    def get_next_step(self) -> WorkflowStep | None:
        for step in self.steps:
            if step.status == StepStatus.FAILED:
                return step

        for step in self.steps:
            if step.status == StepStatus.PENDING:
                return step

        return None

    def start_step(self, step_name: str) -> None:
        self.update_step(
            step_name,
            StepStatus.RUNNING
        )

    def complete_step(self, step_name: str) -> None:
        self.update_step(
            step_name,
            StepStatus.COMPLETED,
        )
