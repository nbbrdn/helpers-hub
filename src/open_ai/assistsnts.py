import time
from openai import OpenAI

finish_states = [
    "requires_action",
    "cancelling",
    "cancelled",
    "failed",
    "completed",
    "expired",
]


def get_client(api_key):
    return OpenAI(api_key)


def create_thread(client):
    thread = client.beta.threads.create()
    return thread.id


def generate_text(client, assistant_id, prompt, thread_id) -> str:
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )

    keep_retrieving_status = None

    while keep_retrieving_status not in finish_states:
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run.id
        )
        keep_retrieving_status = keep_retrieving_run.status

        if keep_retrieving_status == "completed":
            break
        time.sleep(3)

    if keep_retrieving_status != "completed":
        return "Ой... что-то пошло не так :("

    all_messages = client.beta.threads.messages.list(thread_id=thread_id)
    return all_messages.data[0].content[0].text.value
