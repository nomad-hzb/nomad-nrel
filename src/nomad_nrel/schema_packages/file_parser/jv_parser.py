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

from io import StringIO

import numpy as np
import pandas as pd


def get_jv_data_nrel(filedata, file_name):
    # Block to clean up some bad characters found in the file which gives
    # trouble reading.

    filedata = filedata.replace('²', '^2')

    df_header = pd.read_csv(
        StringIO(filedata),
        skiprows=2,
        nrows=15,
        header=None,
        sep=': ',
        index_col=0,
        encoding='unicode_escape',
        engine='python',
    )
    df_curves = pd.read_csv(
        StringIO(filedata),
        header=17,
        skiprows=[16],
        sep='\t',
        encoding='unicode_escape',
        engine='python',
    )

    df_curves = df_curves.dropna(how='all', axis=1)

    df_header.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

    jv_dict = {}
    jv_dict['active_area'] = float(df_header.iloc[7, 0].split(' ')[0])
    jv_dict['intensity'] = float(df_header.iloc[1, 0]) * 100

    jv_dict['jv_curve'] = []

    jv_dict['jv_curve'].append(
        {
            'name': ' '.join(file_name.split('_')[3:7]),
            'voltage': df_curves['Voltage'].values,
            'current_density': df_curves['Current'].values,
        }
    )

    return jv_dict
