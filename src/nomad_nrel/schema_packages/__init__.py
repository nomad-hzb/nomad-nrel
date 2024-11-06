from nomad.config.models.plugins import SchemaPackageEntryPoint


class NRELPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_nrel.schema_packages.nrel_package import m_package

        return m_package


nrel_package = NRELPackageEntryPoint(
    name='NREL',
    description='Package for NREL Lab',
)
