# https://github.com/apache/nifi/tree/main/nifi-framework-bundle/nifi-framework-extensions/nifi-py4j-framework-bundle/nifi-python-extension-api/src/main/python/src/nifiapi
from nifiapi.flowfilesource import FlowFileSource, FlowFileSourceResult
from nifiapi.relationship import Relationship

import random
import string
import time
import uuid

# import some libraries which contains C extension
import paramiko
import numpy as np
from scipy import linalg, integrate

def linear_algebra_demo():
    # Prosty układ Ax = b
    A = np.array([[3.0, 1.0], [1.0, 2.0]])
    b = np.array([9.0, 8.0])
    x = linalg.solve(A, b)  # używa scipy.linalg (optymalizacje BLAS/LAPACK jeśli dostępne)
    eigvals, eigvecs = linalg.eig(A)
    return A, b, x, eigvals


def integration_demo():
    # Całka ∫_0^π sin(x) dx = 2
    f = lambda x: np.sin(x)
    value, error = integrate.quad(f, 0, np.pi)
    return value, error


class WriteHelloWorld(FlowFileSource):
    class Java:
        implements = ['org.apache.nifi.python.processor.FlowFileSource']
    class ProcessorDetails:
        version = '0.0.1-SNAPSHOT'
        dependencies = ['paramiko', 'numpy', 'scipy']
        description = "Example python module"
        tags = ["test1", "test2"]

    REL_SUCCESS = Relationship(name="success", description="Successful FlowFiles")
    relationships = frozenset([REL_SUCCESS])

    def getRelationships(self):
        return self.relationships

    def getSupportedPropertyDescriptors(self):
        return []

    def __init__(self, **kwargs):
        pass

    def create(self, context):
        self.logger.info(str(linear_algebra_demo()))
        self.logger.info(str(integration_demo()))
        return FlowFileSourceResult(relationship = WriteHelloWorld.REL_SUCCESS.name, contents = "Hello World", attributes = {"greeting": "hello"})
