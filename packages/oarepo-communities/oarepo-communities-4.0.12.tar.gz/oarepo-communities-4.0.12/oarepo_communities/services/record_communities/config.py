from invenio_indexer.api import RecordIndexer
from invenio_records_resources.services.base.config import (
    ConfiguratorMixin,
    ServiceConfig,
)
from oarepo_runtime.services.config.service import PermissionsPresetsConfigMixin

from .schema import RecordCommunitiesSchema


class RecordCommunitiesServiceConfig(
    PermissionsPresetsConfigMixin, ServiceConfig, ConfiguratorMixin
):
    """Record communities service config."""

    service_id = ""

    schema = RecordCommunitiesSchema
    indexer_cls = RecordIndexer
    indexer_queue_name = service_id
    index_dumper = None

    # todo do we need this?
    # Max n. communities that can be added at once
    max_number_of_additions = 10
    # Max n. communities that can be removed at once
    max_number_of_removals = 10
