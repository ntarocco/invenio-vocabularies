# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2024 CERN.
#
# Invenio-Vocabularies is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Jobs module."""

import datetime

from invenio_i18n import gettext as _
from invenio_jobs.jobs import JobType

from invenio_vocabularies.services.tasks import process_datastream


class ProcessDataStreamJob(JobType):
    """Generic process data stream job type."""

    task = process_datastream


class ProcessRORAffiliationsJob(ProcessDataStreamJob):
    """Process ROR affiliations datastream registered task."""

    description = "Process ROR affiliations"
    title = "Load ROR affiliations"
    id = "process_ror_affiliations"

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs):
        """Process ROR affiliations."""
        # NOTE: Update is set to False for now given we don't have the logic to re-index dependent records yet.
        # Since jobs support custom args, update true can be passed via that.
        return {
            "config": {
                "readers": [
                    {
                        "args": {"since": str(since)},
                        "type": "ror-http",
                    },
                    {"args": {"regex": "_schema_v2\\.json$"}, "type": "zip"},
                    {"type": "json"},
                ],
                "writers": [
                    {
                        "args": {
                            "writer": {
                                "type": "affiliations-service",
                                "args": {"update": False},
                            }
                        },
                        "type": "async",
                    }
                ],
                "transformers": [{"type": "ror-affiliations"}],
            }
        }


class ProcessRORFundersJob(ProcessDataStreamJob):
    """Process ROR funders datastream registered task."""

    description = "Process ROR funders"
    title = "Load ROR funders"
    id = "process_ror_funders"

    @classmethod
    def build_task_arguments(cls, job_obj, since=None, **kwargs):
        """Process ROR funders."""
        # NOTE: Update is set to False for now given we don't have the logic to re-index dependent records yet.
        # Since jobs support custom args, update true can be passed via that.
        return {
            "config": {
                "readers": [
                    {
                        "args": {"since": str(since)},
                        "type": "ror-http",
                    },
                    {"args": {"regex": "_schema_v2\\.json$"}, "type": "zip"},
                    {"type": "json"},
                ],
                "writers": [
                    {
                        "args": {
                            "writer": {
                                "type": "funders-service",
                                "args": {"update": False},
                            }
                        },
                        "type": "async",
                    }
                ],
                "transformers": [{"type": "ror-funders"}],
            }
        }
