from pytest import fixture

from plp import Renderer


@fixture(name='r')
def renderer():
    return Renderer()
