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

import random
import string

from baseclasses import (
    BaseMeasurement,
    BaseProcess,
    Batch,
    LayerDeposition,
)
from baseclasses.material_processes_misc import (
    Cleaning,
    LaserScribing,
    PlasmaCleaning,
    SolutionCleaning,
    UVCleaning,
)
from baseclasses.solar_energy import (
    BasicSampleWithID,
    EQEMeasurement,
    JVMeasurement,
    SolcarCellSample,
    Substrate,
)
from baseclasses.solution import Ink, Solution, SolutionPreparationStandard
from baseclasses.vapour_based_deposition import (
    ALDPropertiesIris,
    AtomicLayerDeposition,
    Evaporations,
    Sputtering,
)
from baseclasses.voila import VoilaNotebook
from baseclasses.wet_chemical_deposition import (
    BladeCoating,
    DipCoating,
    LP50InkjetPrinting,
    SlotDieCoating,
    SpinCoating,
    WetChemicalDeposition,
)
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.plot import PlotlyFigure, PlotSection
from nomad.metainfo import (
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
)

m_package = SchemaPackage()


# %% ####################### Entities


def randStr(chars=string.ascii_uppercase + string.digits, N=6):
    return ''.join(random.choice(chars) for _ in range(N))


class NREL_VoilaNotebook(VoilaNotebook, EntryData):
    m_def = Section(a_eln=dict(hide=['lab_id']))

    def normalize(self, archive, logger):
        super().normalize(archive, logger)


class NREL_Substrate(Substrate, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'components', 'elemental_composition'],
            properties=dict(
                order=[
                    'name',
                    'substrate',
                    'conducting_material',
                    'solar_cell_area',
                    'pixel_area',
                    'number_of_pixels',
                ]
            ),
        )
    )


class NREL_Solution(Solution, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'users',
                'components',
                'elemental_composition',
                'method',
                'temperature',
                'time',
                'speed',
                'solvent_ratio',
                'washing',
            ],
            properties=dict(
                order=[
                    'name',
                    'datetime',
                    'lab_id',
                    'description',
                    'preparation',
                    'solute',
                    'solvent',
                    'other_solution',
                    'additive',
                    'storage',
                ],
            ),
        ),
        a_template=dict(temperature=45, time=15, method='Shaker'),
    )

    preparation = SubSection(section_def=SolutionPreparationStandard)


class NREL_Ink(Ink, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['users', 'components', 'elemental_composition', 'chemical_formula'],
            properties=dict(
                order=[
                    'name',
                    'method',
                    'temperature',
                    'time',
                    'speed',
                    'solvent_ratio',
                ]
            ),
        ),
        a_template=dict(temperature=45, time=15, method='Shaker'),
    )


class NREL_Sample(SolcarCellSample, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['users', 'components', 'elemental_composition'],
            properties=dict(order=['name', 'substrate', 'architecture']),
        ),
        label_quantity='sample_id',
    )


class NREL_BasicSample(BasicSampleWithID, EntryData):
    m_def = Section(
        a_eln=dict(hide=['users', 'components', 'elemental_composition']),
        label_quantity='sample_id',
    )


class NREL_Batch(Batch, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['users', 'samples'],
            properties=dict(order=['name', 'export_batch_ids', 'csv_export_file']),
        )
    )


# %% ####################### Cleaning
class NREL_Cleaning(Cleaning, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'datetime',
                    'previous_process',
                    'batch',
                    'samples',
                ]
            ),
        )
    )

    cleaning = SubSection(section_def=SolutionCleaning, repeats=True)
    cleaning_uv = SubSection(section_def=UVCleaning, repeats=True)
    cleaning_plasma = SubSection(section_def=PlasmaCleaning, repeats=True)


# %% ### Printing


class NREL_Inkjet_Printing(LP50InkjetPrinting, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'recipe_used',
                    'print_head_used',
                    'datetime',
                    'previous_process',
                    'batch',
                    'samples',
                    'solution',
                    'layer',
                    'properties',
                    'print_head_path',
                    'nozzle_voltage_profile',
                    'quenching',
                    'annealing',
                ]
            ),
        ),
        a_template=dict(
            layer_type='Absorber Layer',
        ),
    )


# %% ### Spin Coating
class NREL_SpinCoating(SpinCoating, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'end_time',
                'steps',
                'instruments',
                'results',
                'recipe',
            ],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'recipe' 'datetime',
                    'previous_process',
                    'batch',
                    'samples',
                    'solution',
                    'layer',
                    'quenching',
                    'annealing',
                ]
            ),
        ),
        a_template=dict(
            layer_type='Absorber Layer',
        ),
    )


# %% ### Dip Coating


class NREL_DipCoating(DipCoating, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'datetime',
                    'batch',
                    'samples',
                    'solution',
                    'layer',
                    'quenching',
                    'annealing',
                ]
            ),
        ),
        a_template=dict(
            layer_type='Absorber Layer',
        ),
    )


class NREL_BladeCoating(BladeCoating, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'datetime',
                    'batch',
                    'samples',
                    'solution',
                    'layer',
                    'quenching',
                    'annealing',
                ]
            ),
        )
    )


# %% ### Slot Die Coating


class NREL_SlotDieCoating(SlotDieCoating, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'author',
                'end_time',
                'steps',
                'instruments',
                'results',
            ],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'datetime',
                    'previous_process',
                    'batch',
                    'samples',
                    'solution',
                    'layer',
                    'properties',
                    'quenching',
                    'annealing',
                ]
            ),
        ),
        a_template=dict(layer_type='Absorber Layer'),
    )


# %% ### Sputterring
class NREL_Sputtering(Sputtering, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'datetime',
                    'batch',
                    'samples',
                    'layer',
                ]
            ),
        )
    )


# %% ### AtomicLayerDepositio


class NREL_AtomicLayerDeposition(AtomicLayerDeposition, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'datetime',
                    'batch',
                    'samples',
                    'layer',
                ]
            ),
        )
    )

    properties = SubSection(section_def=ALDPropertiesIris)


# %% ### Evaporation
class NREL_Evaporation(Evaporations, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=[
                    'name',
                    'location',
                    'present',
                    'datetime',
                    'batch',
                    'samples',
                    'layer',
                ]
            ),
        )
    )


# %% ## Laser Scribing
class NREL_LaserScribing(LaserScribing, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=['lab_id', 'users', 'end_time', 'steps', 'instruments', 'results'],
            properties=dict(
                order=['name', 'location', 'present', 'datetime', 'batch', 'samples']
            ),
        )
    )


class NREL_JVmeasurement(JVMeasurement, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'solution',
                'users',
                'author',
                'certified_values',
                'certification_institute',
                'end_time',
                'steps',
                'instruments',
                'results',
            ],
            properties=dict(
                order=[
                    'name',
                    'data_file',
                    'active_area',
                    'intensity',
                    'integration_time',
                    'settling_time',
                    'averaging',
                    'compliance',
                    'samples',
                ]
            ),
        ),
        a_plot=[
            {
                'x': 'jv_curve/:/voltage',
                'y': 'jv_curve/:/current_density',
                'layout': {
                    'showlegend': True,
                    'yaxis': {'fixedrange': False},
                    'xaxis': {'fixedrange': False},
                },
            }
        ],
    )

    data_files = Quantity(
        type=str,
        shape=['*'],
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'),
    )

    def normalize(self, archive, logger):
        from baseclasses.solar_energy.jvmeasurement import (
            SolarCellJVCurveCustom,
        )

        from nomad_nrel.schema_packages.file_parser.jv_parser import (
            get_jv_data_nrel,
        )

        if self.data_files:
            curves = []
            for file in self.data_files:
                with archive.m_context.raw_file(file, 'tr') as f:
                    jv_dict = get_jv_data_nrel(f.read(), file)
                    curves.extend(jv_dict['jv_curve'])
            jv_dict['jv_curve'] = curves

            self.active_area = (
                jv_dict['active_area'] if 'active_area' in jv_dict else None
            )
            self.intensity = jv_dict['intensity'] if 'intensity' in jv_dict else None

            jv_curve = []
            for curve_idx, curve in enumerate(jv_dict['jv_curve']):
                jv_set = SolarCellJVCurveCustom(
                    cell_name=curve['name'],
                    voltage=curve['voltage'],
                    current_density=curve['current_density'],
                )
                jv_set.normalize(archive, logger)
                jv_curve.append(jv_set)

            self.jv_curve = jv_curve

        super().normalize(archive, logger)


class NREL_JVmeasurementStability(JVMeasurement, PlotSection, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'solution',
                'users',
                'author',
                'certified_values',
                'certification_institute',
                'end_time',
                'steps',
                'instruments',
                'results',
            ],
            properties=dict(
                order=[
                    'name',
                    'data_file',
                    'active_area',
                    'intensity',
                    'integration_time',
                    'settling_time',
                    'averaging',
                    'compliance',
                    'samples',
                ]
            ),
        ),
    )

    def normalize(self, archive, logger):
        import plotly.graph_objects as go
        from baseclasses.solar_energy.jvmeasurement import (
            SolarCellJVCurveCustom,
        )

        from nomad_nrel.schema_packages.file_parser.jv_parser import (
            get_jv_data_stability_nrel,
        )

        if self.data_file:
            with archive.m_context.raw_file(self.data_file, 'tr') as f:
                jv_dict = get_jv_data_stability_nrel(f.read())

            jv_curve = []
            for curve_idx, curve in enumerate(jv_dict['curves']):
                jv_set = SolarCellJVCurveCustom(
                    light_intensity=100 * float(curve['Light']),
                    cell_name=curve['Timestamp'],
                    voltage=curve['data']['voltage'] * -1,
                    current_density=curve['data']['current']
                    * 1000
                    / float(jv_dict['PxSize']),
                )
                jv_set.normalize(archive, logger)
                jv_curve.append(jv_set)

            self.jv_curve = jv_curve

            fig1 = go.Figure()
            fig1.add_trace(
                go.Scatter(
                    x=[
                        int(x.get('cell_name'))
                        if x.get('cell_name').isdigit()
                        else None
                        for x in self.jv_curve
                    ],
                    y=[x.get('efficiency') for x in self.jv_curve],
                    name='Efficiency over timestamps',
                    marker=dict(color='blue'),
                )
            )
            self.figures = [
                PlotlyFigure(
                    label='Efficiency over timestamps',
                    index=2,
                    open=True,
                    figure=fig1.to_plotly_json(),
                )
            ]

        super().normalize(archive, logger)


class NREL_EQEmeasurement(EQEMeasurement, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'solution',
                'users',
                'location',
                'end_time',
                'steps',
                'instruments',
                'results',
                'data',
                'header_lines',
            ],
            properties=dict(order=['name', 'data_file', 'samples']),
        ),
        a_plot=[
            {
                'x': 'eqe_data/:/photon_energy_array',
                'y': 'eqe_data/:/eqe_array',
                'layout': {
                    'showlegend': True,
                    'yaxis': {'fixedrange': False},
                    'xaxis': {'fixedrange': False},
                },
            }
        ],
    )

    def normalize(self, archive, logger):
        # from nomad_hysprint.schema_packages.file_parser.eqe_parser import (
        #     read_file_multiple,
        # )

        # if self.data_file:
        #     with archive.m_context.raw_file(self.data_file, 'br') as f:
        #         encoding = get_encoding(f)
        #     with archive.m_context.raw_file(
        #         self.data_file, 'tr', encoding=encoding
        #     ) as f:
        #         data_list = read_file_multiple(f.read())
        #     eqe_data = []
        #     for d in data_list:
        #         entry = SolarCellEQECustom(
        #             photon_energy_array=d.get('photon_energy'),
        #             raw_photon_energy_array=d.get('photon_energy_raw'),
        #             eqe_array=d.get('intensity'),
        #             raw_eqe_array=d.get('intensty_raw'),
        #         )
        #         entry.normalize(archive, logger)
        #         eqe_data.append(entry)
        #     self.eqe_data = eqe_data

        # if eqe_data:
        #     band_gaps = np.array([d.bandgap_eqe.magnitude for d in eqe_data])

        #     add_band_gap(archive, band_gaps[np.isfinite(band_gaps)].mean())

        super().normalize(archive, logger)


# %%####################################### Generic Entries


class NREL_Process(BaseProcess, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time',
                'steps',
                'instruments',
                'results',
            ],
            properties=dict(order=['name', 'present', 'data_file', 'batch', 'samples']),
        )
    )

    data_file = Quantity(
        type=str,
        shape=['*'],
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'),
    )


class NREL_WetChemicalDepoistion(WetChemicalDeposition, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time',
                'steps',
                'instruments',
                'results',
            ],
            properties=dict(
                order=[
                    'name',
                    'present',
                    'datetime',
                    'previous_process',
                    'batch',
                    'samples',
                    'solution',
                    'layer',
                    'quenching',
                    'annealing',
                ]
            ),
        )
    )

    data_file = Quantity(
        type=str,
        shape=['*'],
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'),
    )


class NREL_Deposition(LayerDeposition, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time',
                'steps',
                'instruments',
                'results',
            ],
            properties=dict(
                order=[
                    'name',
                    'present',
                    'datetime',
                    'previous_process',
                    'batch',
                    'samples',
                    'layer',
                ]
            ),
        )
    )

    data_file = Quantity(
        type=str,
        shape=['*'],
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'),
    )


class NREL_Measurement(BaseMeasurement, EntryData):
    m_def = Section(
        a_eln=dict(
            hide=[
                'lab_id',
                'users',
                'location',
                'end_time',
                'steps',
                'instruments',
                'results',
            ],
            properties=dict(order=['name', 'data_file', 'samples', 'solution']),
        )
    )

    data_file = Quantity(
        type=str,
        a_eln=dict(component='FileEditQuantity'),
        a_browser=dict(adaptor='RawFileAdaptor'),
    )


m_package.__init_metainfo__()
