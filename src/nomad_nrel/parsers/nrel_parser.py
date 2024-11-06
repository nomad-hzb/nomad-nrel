#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import datetime
import os

from baseclasses.helper.utilities import (
    create_archive,
    get_entry_id_from_file_name,
    get_reference,
    set_sample_reference,
)
from nomad.datamodel import EntryArchive
from nomad.datamodel.data import (
    EntryData,
)
from nomad.datamodel.metainfo.annotations import (
    ELNAnnotation,
)
from nomad.datamodel.metainfo.basesections import (
    Entity,
)
from nomad.metainfo import (
    Quantity,
)
from nomad.parsing import MatchingParser

from nomad_nrel.schema_packages.nrel_package import (
    NREL_JVmeasurement,
)

"""
This is a hello world style example for an example parser/converter.
"""


class RawFileNREL(EntryData):
    processed_archive = Quantity(
        type=Entity,
        a_eln=ELNAnnotation(
            component='ReferenceEditQuantity',
        ),
    )


class NRELJVParser(MatchingParser):
    def parse(self, mainfile: str, archive: EntryArchive, logger):
        # Log a hello world, just to get us started. TODO remove from an actual parser.

        mainfile_split = os.path.basename(mainfile).split('.')

        entry = NREL_JVmeasurement()

        archive.metadata.entry_name = os.path.basename(mainfile)

        search_id = mainfile_split[0]
        set_sample_reference(archive, entry, search_id)

        entry.name = f'{search_id} JV'

        entry.data_file = os.path.basename(mainfile)
        entry.datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        file_name = f'{os.path.basename(mainfile)}.archive.json'
        eid = get_entry_id_from_file_name(file_name, archive)
        archive.data = RawFileNREL(
            processed_archive=get_reference(archive.metadata.upload_id, eid)
        )
        create_archive(entry, archive, file_name)
