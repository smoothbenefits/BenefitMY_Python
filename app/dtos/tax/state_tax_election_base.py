STATE_TAX_DATA_SOURCE_USER = 'User'
STATE_TAX_DATA_SOURCE_IMPORT = 'Import'


class StateTaxElectionBase(object):
    
    ''' As much that I don't like this, this is the simplest
        and most efficient way to workaround a weird requirements
        from Django Rest Serializer. 
        That is, when a parent serializer for a persistent model
        contains a nested serializer for non-persistent model/dto,
        with the current version of Django Rest framework, it does 
        not provide any effective way to say "do not try to save"
        the object created by that nested serializer. As a result,
        the framework would always try to call ".save" on those
        objects, and hence we have to provide it here with an empty
        body...
    '''
    def save(self):
        pass

    @property
    def data_source(self):
        return STATE_TAX_DATA_SOURCE_USER

    @property
    def is_imported(self):
        return self.data_source == STATE_TAX_DATA_SOURCE_IMPORT
