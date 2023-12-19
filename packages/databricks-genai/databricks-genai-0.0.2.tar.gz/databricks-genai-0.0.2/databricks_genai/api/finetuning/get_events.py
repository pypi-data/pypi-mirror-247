"""List events for a finetuning run"""

from typing import Union

from mcli import list_finetuning_events

from databricks_genai.api.config import configure_request
from databricks_genai.types.common import ObjectList
from databricks_genai.types.finetuning import FinetuningEvent, FinetuningRun


@configure_request
def get_events(finetuning_run: Union[str, FinetuningRun]) -> ObjectList[FinetuningEvent]:
    """List finetuning runs
    
    Args:
        finetuning_run (Union[str, FinetuningRun]): The finetuning run to get events for.

    Returns:
        List[FinetuningEvent]: A list of finetuning events. Each event has an event 
            type, time, and message.
    """
    return ObjectList(list_finetuning_events(finetune=finetuning_run), FinetuningEvent)
