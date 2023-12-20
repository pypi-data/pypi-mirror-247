"""
    CALLBACKS
        - python functions executed on specific success/failure events
"""
import logging
from sdc_helpers.slack_helper import SlackHelper
from airflow.models import DAG, TaskInstance

logger = logging.getLogger(None)


def generate_slack_message(
    status: str,
    task: str,
    dag: str,
    exec_date: str,
    log_url: str,
    short_description: str = None,
):
    """generates a slack message from provided dag-task attributes"""
    if status == "success":
        symbol = ":large_green_circle:"
        if short_description is None:
            short_description = "Task Succeeded."
        else:
            short_description = short_description
    elif status == "failure":
        symbol = ":red_circle:"
        if short_description is None:
            short_description = "Task Failed."
        else:
            short_description = short_description
    else:
        symbol = ":warning:"
        if short_description is None:
            short_description = "no detail provided."
        else:
            short_description = short_description
    return f"""
        {symbol} {short_description}
        *Task*: {task}  
        *Dag*: {dag} 
        *Execution Time*: {exec_date}  
        *Log Url*: {log_url}
    """


def slack_notification_success(context):
    """slack success notification"""
    ti = context["task_instance"]
    slack_msg = generate_slack_message(
        status="success",
        task=ti.task_id,
        dag=ti.dag_id,
        exec_date=context.get("execution_date"),
        log_url=ti.log_url,
    )
    slack_helper = SlackHelper()
    slack_helper.send_critical(message=slack_msg)


def slack_notification_failure(context):
    """slack failure notification"""
    ti = context["task_instance"]
    slack_msg = generate_slack_message(
        status="failure",
        task=ti.task_id,
        dag=ti.dag_id,
        exec_date=context.get("execution_date"),
        log_url=ti.log_url,
    )

    slack_helper = SlackHelper()
    slack_helper.send_critical(message=slack_msg)


def slack_notification_retry(context):
    """slack retry notification"""
    ti = context["task_instance"]
    slack_msg = generate_slack_message(
        status="warning",
        task=ti.task_id,
        dag=ti.dag_id,
        exec_date=context.get("execution_date"),
        log_url=ti.log_url,
        short_description="Task up for retry",
    )

    slack_helper = SlackHelper()
    slack_helper.send_critical(message=slack_msg)


def slack_notification_sla(
    dag: DAG,
    task_list: str,
    blocking_task_list: str,
    slas: list,
    blocking_tis: list,
) -> None:
    """Send `SLA missed` alert to Slack"""
    task_instance: TaskInstance = blocking_tis[0]

    slack_msg = generate_slack_message(
        status="warning",
        task=task_instance.task_id,
        dag=dag.dag_id,
        exec_date=f"{task_instance.execution_date.strftime('%Y-%m-%d %H:%M:%S')} UTC",
        log_url=task_instance.log_url,
        short_description=f"""
            *SLA Time*: {task_instance.task.sla}
            *Task State*: `{task_instance.state}`
            """,
    )
    slack_helper = SlackHelper()
    slack_helper.send_critical(message=slack_msg)
