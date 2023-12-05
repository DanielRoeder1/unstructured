import logging
import typing as t
from dataclasses import dataclass

from unstructured.ingest.logger import ingest_log_streaming_init, logger
from unstructured.ingest.runner.base_runner import FsspecBaseRunner
from unstructured.ingest.runner.utils import update_download_dir_remote_url

if t.TYPE_CHECKING:
    from unstructured.ingest.connector.dropbox import SimpleDropboxConfig


@dataclass
class DropboxRunner(FsspecBaseRunner):
    fsspec_config: t.Optional["SimpleDropboxConfig"] = None

    def run(
        self,
        token: t.Optional[str] = None,
        **kwargs,
    ):
        ingest_log_streaming_init(logging.DEBUG if self.processor_config.verbose else logging.INFO)

        self.read_config.download_dir = update_download_dir_remote_url(
            connector_name="dropbox",
            read_config=self.read_config,
            remote_url=self.fsspec_config.remote_url,  # type: ignore
            logger=logger,
        )

        from unstructured.ingest.connector.dropbox import (
            DropboxSourceConnector,
        )

        source_doc_connector = DropboxSourceConnector(  # type: ignore
            read_config=self.read_config,
            connector_config=self.fsspec_config,
            processor_config=self.processor_config,
        )

        self.process_documents(source_doc_connector=source_doc_connector)
