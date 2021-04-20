import pytest
from assertpy import assert_that
from ..quota import Quota
import lware.mongodata as m

q = Quota("TestUtilization")


def test_quota_init():

    res, status = q.init_quota("my_tenant_id", unit_type="cpuq")

    # print(res, status)

    try:
        assert_that(res).is_equal_to({'status': 'success', 'message': 'Quota initialized'})
        assert_that(status).is_equal_to(200)
    except:
        assert_that(res).is_equal_to({'status': 'fail', 'message': 'App already installed'})
        assert_that(status).is_equal_to(400)
    


def test_quota_update():

    res, status = q.update_quota(
        tenant_id="my_tenant_id", 
        unit_type="cpuq", 
        number_of_units=5
    )

    # print(res, status)

    assert_that(res).is_equal_to({'status': 'success', 'message': 'Quota updated'})
    assert_that(status).is_equal_to(200)



def test_check_quota():

    res, status = q.check_quota(
        tenant_id="my_tenant_id", 
        unit_type="cpuq",
    )

    # print(res, status)

    try:
        assert_that(res).is_equal_to({'status': 'success', 'message': 'Utilization within monthly quota'})
        assert_that(status).is_equal_to(200)
    except:
        assert_that(res).is_equal_to({'status': 'fail', 'message': 'Monthly quota exceeded'})
        assert_that(status).is_equal_to(402)


def test_teardown():

    deleted_col_nbr = m.delete(
        collection = "TestUtilization",
        match      = "TestUtilization",
    )

    assert_that(deleted_col_nbr).is_equal_to(1)
