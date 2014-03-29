from .sphinxapi import SphinxClient
import config

sphinx_client = SphinxClient()
sphinx_client.SetServer(str(config.SPHINX['host']), config.SPHINX['port'])

# resets everything and returns the sphinx client
def get_sphinx_client():
    sphinx_client.ResetOverrides()
    sphinx_client.ResetFilters()
    sphinx_client.ResetGroupBy()
    sphinx_client.ResetQueryFlag()
    sphinx_client.ResetOuterSelect();

    return sphinx_client