from nomad.config.models.plugins import ParserEntryPoint


class NRELJVParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_nrel.parsers.nrel_parser import NRELJVParser

        return NRELJVParser(**self.dict())


class NRELExperimentParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_nrel.parsers.nrel_batch_parser import (
            NRELExperimentParser,
        )

        return NRELExperimentParser(**self.dict())


nrel_jv_parser = NRELJVParserEntryPoint(
    name='NRELParser',
    description='Parser for NREL jv files',
    mainfile_name_re='^(.+\.?.+\.((eqe|jv|jvi|pl|pli|hy|spv|env|uvvis|PL|JV|PLI|EQE|SEM|sem|xrd|mppt)\..{1,4})|.+\.nk)$',
    mainfile_mime_re='(application|text|image)/.*',
)


nrel_experiment_parser = NRELExperimentParserEntryPoint(
    name='NRELBatchParser',
    description='Parser for NREL Batch xlsx files',
    mainfile_name_re='^(.+\.xlsx)$',
    mainfile_mime_re='(application|text|image)/.*',
)
