from licenseware.utils.log_config import log
from functools import wraps
# from inspect import iscoroutinefunction, isfunction



def failsafe(*dargs, fail_code=0, success_code=0):
    """
        Prevents a function to raise an exception and break the app.
        Returns a string with the exception and saves the traceback in failsafe.log
        If fail_code or success_code is specified then a json response will be returned.
        
        @failsafe
        def fun1(): raise Exception("test")
        print(fun1())
        # >>test

        @failsafe(fail_code=500)
        def fun2(): raise Exception("test")
        print(fun2())
        # >> ({'status': 'Fail', 'message': 'test'}, 500)

        @failsafe(fail_code=500, success_code=200)
        def fun3(): return "test"
        print(fun3())
        # >> ({'status': 'Success', 'message': 'test'}, 200)
        
    """
    
    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                if success_code:
                    return {"status": "success", "message": response}, success_code
                return response
            except Exception as err:
                log.exception("\n\n\n\n-------------Failsafe traceback:\n\n")
                if fail_code:
                    return {"status": "fail", "message": str(err)}, fail_code
                return str(err)
        return wrapper

    return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator



# TODO failsafe for async functions
# def _failsafe_success(response, success_code):
#     if success_code:
#         return {"status": "success", "message": response}, success_code
#     return response

# def _failsafe_fail(fail_code, error):
#     logger.exception("\n\n\n\n-------------Failsafe traceback:\n\n")
#     if fail_code:
#         return {"status": "fail", "message": str(error)}, fail_code
#     return str(error)


# def failsafe_async(*dargs, fail_code=0, success_code=0):

#     def _decorator(f):

#         if isfunction(f):
#             @wraps(f)
#             def wrapper(*args, **kwargs):
#                 try:
#                     response = f(*args, **kwargs)
#                     return _failsafe_success(response, success_code)
#                 except Exception as error:
#                     return _failsafe_fail(fail_code, error)
#             return wrapper

#         if iscoroutinefunction(f):
#             @wraps(f)
#             async def wrapper(*args, **kwargs):
#                 try:
#                     response = await f(*args, **kwargs)
#                     return _failsafe_success(response, success_code)
#                 except Exception as error:
#                     return _failsafe_fail(fail_code, error)
#             return wrapper
            
#     return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator


