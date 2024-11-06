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
    name='NRELJVParser',
    description='Parser for NREL jv files',
    mainfile_name_re=r'^.*CU_.+_fwd_lt_lp1_.+\.txt$',
    mainfile_mime_re='(application|text|image)/.*',
    mainfile_contents_re=r"""^// \*\*\*\*\*\*\*\*\*\*\*\*\*\* HEADER START \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*""",  # noqa E501
)


nrel_experiment_parser = NRELExperimentParserEntryPoint(
    name='NRELBatchParser',
    description='Parser for NREL Batch xlsx files',
    mainfile_name_re=r'^(.+\.xlsx)$',
    mainfile_mime_re='(application|text|image)/.*',
)
