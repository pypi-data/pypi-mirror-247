import dataclasses
from typing import Any, Dict, List, Optional

import dataclasses_json


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Progress:
    """Descriptor of the training progress to inform the user."""

    epoch: int
    max_epochs: int
    step: int
    max_steps: int
    phase: str
    loss: float
    error: str = None
    done: bool = False


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Identity:
    """Descriptor of the identity of the client."""

    machine_id: str
    uid: str = ''
    devices: Optional[List[Dict[str, Any]]] = None
    remote_address: str = ''
    port: int = 0


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class ComputeInfo:
    """Descriptor of the compute to be executed.

    The graph should be sent separately as a bytes file.
    """

    training: bool
    batch_size: int
    data_len: int
    use_mixed_precision: bool
    states: Dict[str, List[int]]
    num_epochs: Optional[int] = None
    resume_training: Optional[bool] = None
    optimizers: Optional[List[Dict[str, Any]]] = None
    lr_schedulers: Optional[str] = None
    seed: Optional[int] = None # for reproducibility
    eval_freq: Optional[int] = None # in epochs
    client: Optional[str] = None # ip of the customer's client
    ports: Optional[Dict[str, int]] = None # ports of the customer's client servers
    world_size: Optional[int] = None # number of workers
    main_rank_ip: Optional[str] = None # ip of the main rank worker
    main_rank_port: Optional[int] = None # port of the main rank worker
    checkpoint_freq: Optional[int] = None # in epochs
