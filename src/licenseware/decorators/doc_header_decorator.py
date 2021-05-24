


def header_doc_decorator(_api):
    """
        Adds auth parameters to header 
    """
    parser = _api.parser()
    parser.add_argument('Authorization', location='headers')
    parser.add_argument('TenantId', location='headers')
    return parser
