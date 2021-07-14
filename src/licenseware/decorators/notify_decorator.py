# from functools import wraps

#TODO

# def notify_status(f):
#     """
#         Refreshes the authentication token before making a request
#     """

#     @wraps(f)
#     def decorated(*args, **kwargs):
#         try:
            
#             return f(*args, **kwargs)
#         except KeyError:
#             log.warning("Could not refresh token")
#             return {"Could not refresh token"}, 403

#     return decorated
