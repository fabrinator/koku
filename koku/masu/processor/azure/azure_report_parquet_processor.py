#
# Copyright 2020 Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""Processor for Azure Parquet files."""
import logging

import ciso8601
import pyarrow.parquet as pq
import pytz
from tenant_schemas.utils import schema_context

from masu.processor.report_parquet_processor_base import ReportParquetProcessorBase
from masu.util import common as utils
from reporting.provider.azure.models import AzureCostEntryBill
from reporting.provider.azure.models import AzureCostEntryLineItemDailySummary
from reporting.provider.azure.models import PRESTO_LINE_ITEM_TABLE

LOG = logging.getLogger(__name__)

PRESTO_ADDITIONAL_COLUMNS = {
    "UsageDateTime",
    "UsageQuantity",
    "PreTaxCost",
    "InstanceId",
    "SubscriptionGuid",
    "ServiceName",
    "Date",
    "Quantity",
    "CostInBillingCurrency",
    "ResourceId",
    "SubscriptionId",
    "MeterCategory",
    "BillingCurrencyCode",
    "Currency",
}


class AzureReportParquetProcessor(ReportParquetProcessorBase):
    def __init__(self, manifest_id, account, s3_path, provider_uuid, parquet_local_path):
        super().__init__(
            manifest_id=manifest_id,
            account=account,
            s3_path=s3_path,
            provider_uuid=provider_uuid,
            parquet_local_path=parquet_local_path,
            numeric_columns=[
                "usagequantity",
                "quantity",
                "resourcerate",
                "pretaxcost",
                "costinbillingcurrency",
                "effectiveprice",
                "unitprice",
                "paygprice",
            ],
            date_columns=["usagedatetime", "date", "billingperiodstartdate", "billingperiodenddate"],
            table_name=PRESTO_LINE_ITEM_TABLE,
        )

    @property
    def postgres_summary_table(self):
        """Return the mode for the source specific summary table."""
        return AzureCostEntryLineItemDailySummary

    def _generate_column_list(self):
        """Generate column list based on parquet file."""
        parquet_file = self._parquet_path
        column_names = pq.ParquetFile(parquet_file).schema.names
        additional_columns = list(PRESTO_ADDITIONAL_COLUMNS.difference(column_names))
        column_names.extend(additional_columns)
        return column_names

    def create_bill(self, bill_date):
        """Create bill postgres entry."""
        if isinstance(bill_date, str):
            bill_date = ciso8601.parse_datetime(bill_date)
        report_date_range = utils.month_date_range(bill_date)
        start_date, end_date = report_date_range.split("-")

        start_date_utc = ciso8601.parse_datetime(start_date).replace(hour=0, minute=0, tzinfo=pytz.UTC)
        end_date_utc = ciso8601.parse_datetime(end_date).replace(hour=0, minute=0, tzinfo=pytz.UTC)

        provider = self._get_provider()

        with schema_context(self._schema_name):
            AzureCostEntryBill.objects.get_or_create(
                billing_period_start=start_date_utc, billing_period_end=end_date_utc, provider=provider
            )
