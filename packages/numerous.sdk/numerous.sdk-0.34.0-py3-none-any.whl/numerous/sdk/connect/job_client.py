"""Contains the implementation of the job client."""

import json
import logging
import os
import signal
import sys
import threading
from datetime import datetime
from enum import Enum
from types import FrameType, TracebackType
from typing import Any, Callable, Optional

import grpc
from numerous.grpc import spm_pb2
from numerous.grpc.spm_pb2_grpc import SPMStub, TokenManagerStub

from numerous.cli.client import get_client
from numerous.sdk.connect.access_token import RefreshingAccessToken
from numerous.sdk.connect.auth import AccessTokenAuthMetadataPlugin
from numerous.sdk.connect.command_handler import CommandHandler
from numerous.sdk.connect.config import Config
from numerous.sdk.connect.file_manager import FileManager, FileUploadContext
from numerous.sdk.connect.hibernation import HibernationHandler
from numerous.sdk.connect.inputs import (
    HIBERNATE_SELF,
    HibernatingSourceAction,
    InputReader,
)
from numerous.sdk.connect.job_state import JobState
from numerous.sdk.connect.job_utils import JobIdentifier
from numerous.sdk.connect.reader import Reader
from numerous.sdk.connect.subscription import Subscription
from numerous.sdk.connect.writer import Writer
from numerous.sdk.models.job import Job
from numerous.sdk.models.optimization import OptimizationConfiguration
from numerous.sdk.models.parameter import Parameter
from numerous.sdk.models.scenario import Scenario
from numerous.sdk.models.time_setup import TimeSetup


class JobStatus(str, Enum):
    INITIALIZING = "initializing"
    RUNNING = "running"
    STOPPED = "stopped"
    FINISHED = "finished"
    ERROR = "error"
    FAILED = "failed"


class JobLogHandler(logging.Handler):
    def __init__(
        self,
        spm: SPMStub,
        identity: JobIdentifier,
        execution_id: str,
        current_root_log_level: int = 0,
    ) -> None:
        super().__init__()
        self._spm_client = spm
        self._project_id = identity.project_id
        self._scenario_id = identity.scenario_id
        self._execution_id = execution_id
        self._previous_root_log_level = current_root_log_level

    def emit(self, record) -> None:
        if logging.Logger.root.level <= record.levelno:
            self._spm_client.PushExecutionLogEntries(
                spm_pb2.LogEntries(
                    execution_id=self._execution_id,
                    log_entries=[
                        "{level}: {record}".format(level=self.level, record=record.msg)
                    ],
                    timestamps=[datetime.utcnow().timestamp()],
                    scenario=self._scenario_id,
                    project_id=self._project_id,
                )
            )

    def get_previous_root_level(self) -> int:
        return self._previous_root_log_level


def _clamp(value: float, minimum: float, maximum: float):
    """Clamps the given value, between the given minimum and maximum values.

    :param minimum: The result will never be lower than the minimum.
    :param maximum: The result will never be higher than the maximum.
    """
    return min(max(minimum, value), maximum)


class JobClient:
    """The JobClient is the recommended way to connect to the numerous platform."""

    def __init__(
        self,
        channel: grpc.Channel,
        identity: JobIdentifier,
        execution_id: str,
        config: Optional[Config] = None,
    ):
        """Initialize the job client with a gRPC channel. The channel must be
        configured with credentials.

        :param channel: A gRPC channel configured with required authorization.
        :param identity: Contains identity information for the job object and related objects.
        """
        self._config = Config() if config is None else config
        self._channel = channel
        self._spm_client = SPMStub(self._channel)
        self._identity = identity
        self._execution_id = execution_id
        self._logger: logging.Logger = self._log_init()
        self._file_manager = FileManager(
            self._spm_client, self._identity.project_id, self._identity.scenario_id
        )
        self._status: JobStatus = JobStatus.INITIALIZING
        self._progress: float = 0.0
        self._message: str = ""
        self._job_state: Optional[JobState] = None
        self._job = None
        self._scenario_document: Optional[dict[str, Any]] = None
        self._scenario: Optional[Scenario] = None
        self._reader: Optional[Reader] = None
        self._input_reader: Optional[InputReader] = None
        self._writer: Optional[Writer] = None
        self._terminate_callback: Optional[Callable] = None
        self._setup_sigterm_handling()

        def set_last_read_key() -> None:
            if self._input_reader:
                self._input_reader.store_last_read_key()

        self._hibernation_handler = HibernationHandler(
            lambda: self.state, set_last_read_key
        )
        self._command_handler = self._create_command_handler(self._hibernation_handler)

    def _setup_sigterm_handling(self):
        def _sigterm_handler(signalnum: int, frame: Optional[FrameType]):  # noqa: F841
            if self._hibernation_handler.hibernating:
                sys.exit(0)

            if self._terminate_callback:
                thread = threading.Thread(target=self._terminate_callback, daemon=True)
                thread.start()
                thread.join(timeout=self._config.terminate_handler_timeout)
            sys.exit(1)

        signal.signal(signal.SIGTERM, _sigterm_handler)

    def _create_command_handler(
        self, hibernating_handler: HibernationHandler
    ) -> CommandHandler:
        subscription = Subscription(
            self._identity.project_id,
            self._identity.scenario_id,
            self._spm_client,
            ".".join(
                (
                    "COMMAND",
                    self._identity.project_id,
                    self._identity.scenario_id,
                    self._identity.job_id,
                )
            ),
        )
        return CommandHandler(subscription, hibernating_handler)

    def _log_init(self) -> logging.Logger:
        """Job Client Log Initialization"""
        job_client_logger = logging.getLogger("job_client")
        job_client_logger.setLevel(logging.INFO)
        self._add_job_log_handler_to_root()
        return job_client_logger

    def _add_job_log_handler_to_root(self):
        root_level = logging.Logger.root.level
        if not logging.Logger.root.hasHandlers():
            logging.Logger.root.setLevel(logging.INFO)
        logging.Logger.root.addHandler(
            JobLogHandler(
                self._spm_client, self._identity, self._execution_id, root_level
            )
        )

    def _remove_job_log_handler_from_root(self):
        job_log_handler = next(
            (item for item in logging.root.handlers if isinstance(item, JobLogHandler)),
            None,
        )
        if job_log_handler is not None:
            logging.Logger.root.handlers.remove(job_log_handler)
            logging.Logger.root.setLevel(job_log_handler.get_previous_root_level())

    def __enter__(self) -> "JobClient":
        """Return itself upon entering the context manager."""
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],  # noqa: F841
        exc_value: Optional[BaseException],  # noqa: F841
        traceback: Optional[TracebackType],  # noqa: F841
    ) -> Optional[bool]:
        """Closes the gRPC channel upon exiting the context manager."""
        self.close()
        return None

    @staticmethod
    def channel_options(config: Config) -> list[tuple[str, Any]]:
        """Returns the default gRPC channel options."""
        return [
            ("grpc.max_message_length", config.grpc_max_message_size),
            ("grpc.max_send_message_length", config.grpc_max_message_size),
            ("grpc.max_receive_message_length", config.grpc_max_message_size),
        ]

    @staticmethod
    def from_connection_params(
        hostname: str,
        port: str,
        refresh_token: str,
        identity: JobIdentifier,
        execution_id: str,
        config: Config,
    ) -> "JobClient":
        """Create a JobClient from connection parameters.

        :param hostname: Hostname of the numerous server
        :param port: gRPC port of the numerous server
        :param refresh_token: Refresh token for the execution.
        :param identity: Contains identity information for the job object and related objects.
        """
        token_manager = TokenManagerStub(
            grpc.secure_channel(
                f"{hostname}:{port}",
                grpc.ssl_channel_credentials(),
                JobClient.channel_options(config),
            )
        )

        authorized_channel = grpc.secure_channel(
            f"{hostname}:{port}",
            grpc.composite_channel_credentials(
                grpc.ssl_channel_credentials(),
                grpc.metadata_call_credentials(
                    AccessTokenAuthMetadataPlugin(
                        RefreshingAccessToken(token_manager, refresh_token)
                    )
                ),
            ),
            JobClient.channel_options(config),
        )

        return JobClient(authorized_channel, identity, execution_id, config)

    @staticmethod
    def _from_environment() -> "JobClient":
        """Create a JobClient from environment variables.

        Uses the following environment variables:
         - `NUMEROUS_API_SERVER`
         - `NUMEROUS_API_PORT`
         - `NUMEROUS_API_REFRESH_TOKEN`
         - `NUMEROUS_PROJECT`
         - `NUMEROUS_SCENARIO`
         - `JOB_ID`
         - `NUMEROUS_EXECUTION_ID`
        """
        return JobClient.from_connection_params(
            os.environ["NUMEROUS_API_SERVER"],
            os.environ["NUMEROUS_API_PORT"],
            os.environ["NUMEROUS_API_REFRESH_TOKEN"],
            JobIdentifier(
                os.environ["NUMEROUS_PROJECT"],
                os.environ["NUMEROUS_SCENARIO"],
                os.environ["JOB_ID"],
            ),
            os.environ["NUMEROUS_EXECUTION_ID"],
            config=Config.from_environment(),
        )

    @staticmethod
    def _from_legacy_client(client: Any) -> "JobClient":
        """Create a JobClient from a legacy :class:`~numerous.client.numerous_client.NumerousClient`.

        Connects to the same job as the legacy client is connected to.
        """
        from numerous.client import NumerousClient
        from numerous.client.common import initialize_grpc_channel

        if not isinstance(client, NumerousClient):
            raise TypeError(
                f"'client' argument must be of type NumerousClient, was {type(client).__name__}"
            )
        else:
            channel, _ = initialize_grpc_channel(
                refresh_token=client.refresh_token,
                token_callback=client._get_current_token,
                server=client._channel_server,
                port=client._channel_port,
                secure=client._channel_secure,
                instance_id=client._instance_id,
            )

            return JobClient(
                channel,
                JobIdentifier(client._project, client._scenario, client._job_id),
                client._execution_id,
                Config.from_environment(),
            )

    def open_output_file(self, file_name: str) -> FileUploadContext:
        """
        :param file_name: Output file name.
        :return: An object to be used under with statement.

        Example:
            >>> with JobClient.connect() as client:
            ...     with client.open_output_file("output_data") as output_file:
            ...         output_file.write("First file content")
            ...         output_file.write_from_file("first_file.csv")
            ...         output_file.write("Second file content")
            ...         output_file.write_from_file("second_file.csv")
        """
        return FileUploadContext(self._file_manager, file_name)

    def close(self) -> None:
        """Close the JobClient.

        Closes the JobClient's connection to the numerous platform, immediately
        terminating any active communication.

        This method is idempotent.
        """

        self._remove_job_log_handler_from_root()

        if self._writer is not None:
            self._writer.close()

        self._channel.close()
        self._command_handler.close()

    @staticmethod
    def connect() -> "JobClient":
        """Create a JobClient from environment variables.

        Uses the following environment variables:
         - `NUMEROUS_API_SERVER`
         - `NUMEROUS_API_PORT`
         - `NUMEROUS_API_REFRESH_TOKEN`
         - `NUMEROUS_PROJECT`
         - `NUMEROUS_SCENARIO`
         - `JOB_ID`
         - `NUMEROUS_EXECUTION_ID`
        """
        try:
            return JobClient._from_environment()
        except KeyError:
            client = get_client()
            return JobClient._from_legacy_client(client)

    @property
    def log(self) -> logging.Logger:
        """Return the Job Client logger for the job."""
        return self._logger

    @property
    def file_manager(self) -> FileManager:
        """Access the file manager of the job."""
        return self._file_manager

    @property
    def state(self) -> JobState:
        """The job state, which can be persisted across hibernations.

        It is a lazy property, that will load any remote state on access.
        """
        if self._job_state is None:
            self._job_state = JobState(
                self._spm_client, self._identity, self._execution_id
            )
        return self._job_state

    @property
    def parameters(self) -> dict[str, Parameter]:
        return self.job.parameters

    @property
    def scenario(self) -> Scenario:
        """The associated :class:`Scenario` configuration, with jobs, components,
        parameters and input variables.

        It is a lazy property, that will load the scenario data on access.
        """
        if self._scenario_document is None:
            self._scenario_document = self._get_scenario_document()

        if self._scenario is None:
            scenario_has_optimization_target = self._scenario_document.get(
                "optimizationTargetScenarioID", False
            )
            optimization = (
                OptimizationConfiguration(
                    self._spm_client,
                    self._identity.project_id,
                    self._identity.scenario_id,
                    self._scenario_document,
                )
                if scenario_has_optimization_target
                else None
            )

            self._scenario = Scenario.from_document(
                self._scenario_document, optimization
            )
        return self._scenario

    @property
    def time_setup(self) -> TimeSetup:
        """The associated time setup of the job, which contains start and end times
        of the simulation, and the duration.
        """
        return self.job.time_setup

    def _get_scenario_document(self) -> dict[str, Any]:
        if self._scenario_document is None:
            response = self._spm_client.GetScenario(
                spm_pb2.Scenario(
                    project=self._identity.project_id,
                    scenario=self._identity.scenario_id,
                )
            )
            self._scenario_document = json.loads(response.scenario_document)
        return self._scenario_document

    @property
    def status(self) -> JobStatus:
        """Status of the job, reported to the platform.

        Getting the status returns a locally cached value.
        """
        return self._status

    @status.setter
    def status(self, value: JobStatus) -> None:
        self._status = value
        self._set_scenario_progress()

    @property
    def message(self) -> str:
        """Status message of the job, reported to the platform. Is truncated to at most 32 characters upon setting.

        Getting the status message returns a locally cached value.
        """
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value[: self._config.max_status_message_length]
        self._set_scenario_progress()

    @property
    def progress(self) -> float:
        """Progress of the job, reported to the platform. Is clamped between 0.0 and 100.0 upon setting.

        Getting the progress returns a locally cached value.
        """
        return self._progress

    @progress.setter
    def progress(self, value: float):
        self._progress = _clamp(value, 0.0, 100.0)
        self._set_scenario_progress()

    def _set_scenario_progress(self):
        self._spm_client.SetScenarioProgress(
            spm_pb2.ScenarioProgress(
                project=self._identity.project_id,
                scenario=self._identity.scenario_id,
                job_id=self._identity.job_id,
                status=self._status.value,
                progress=self._progress,
                message=self._message,
            )
        )

    @property
    def reader(self) -> Reader:
        """Data reader for the job."""
        if self._reader is None:
            self._reader = Reader(
                self._spm_client,
                self._identity,
                self._execution_id,
            )
        return self._reader

    @property
    def writer(self) -> Writer:
        """Data writer for the job."""
        if self._writer is None:
            self._writer = Writer(
                self._spm_client,
                self._identity,
                self._execution_id,
                self._config.grpc_max_message_size,
                flush_margin_bytes=self._config.grpc_max_message_size // 8,
            )

        return self._writer

    def set_terminate_callback(self, callback: Callable[[], Any]) -> None:
        """Set a custom function to be called if the job is terminated."""
        self._terminate_callback = callback

    def set_hibernate_callback(self, callback: Callable[[], Any]) -> None:
        """Set a custom function to be called if the job is hibernated."""
        self._hibernation_handler.callback = callback

    @property
    def job(self) -> Job:
        """The model of the current job."""
        return self.scenario.jobs[self._identity.job_id]

    def read_inputs(
        self,
        step: float,
        repeat_spacing: Optional[float] = None,
        hibernating_source_action: HibernatingSourceAction = HIBERNATE_SELF,
    ) -> InputReader:
        """Get an iterator over all input variables in the scenario.

        This method can only be called once in the job runtime.

        :param step: The distance (in time) between each read. Zero-order hold is used
            for values at steps that are not in the original data set.
        :param repeat_spacing: The distance (in time) between the last data point of the
            source data set, and the repeated first data point when repeating.

        Returns an :class:`~numerous.sdk.connect.inputs.InputReader`, that can be
        iterated over.

        Example:
            >>> result = 0
            >>> with JobClient.connect() as job_client:
            ...     for t, data in job_client.read_inputs(step=3600.0):
            ...          result += data["component_name.input_variable_id"]
        """

        if self._input_reader:
            raise RuntimeError("You can only read inputs once during a job runtime.")

        self._input_reader = InputReader(
            self._spm_client,
            hibernation_handler=self._hibernation_handler,
            input_sources=self.scenario.input_sources,
            input_variables=self.scenario.input_variables,
            identity=self._identity,
            execution_id=self._execution_id,
            job=self.job,
            step=step,
            repeat_spacing=repeat_spacing,
            hibernating_source_action=hibernating_source_action,
        )
        return self._input_reader
