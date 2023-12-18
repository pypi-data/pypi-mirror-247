from typing import Optional

from xflow._utils.decorators import client_method
from xflow.model.structures import ModelSignature
# from xflow.deploy.types import InstanceType
import xflow._private.client as xflow_client
import xflow._utils.request_util as req_util
from xflow._private._constants import RequestPath
import xflow._private.request_vo as req_vo
from xflow.deploy.util import validate_converter


@client_method
def export_converter(name: str, script_file: str, converter_input: list[ModelSignature],
                     converter_output: list[ModelSignature],
                     requirements_file: Optional[str] = None,
                     # instance_type: Optional[str] = InstanceType.CPU,
                     namespace: str = "default", backend: Optional[str] = "python3.11",):
    print(f"exporting...")
    # if instance_type not in list(InstanceType().__dict__.values()):
    #     raise ValueError(f"unsupported instance type {instance_type}. use InstanceType class in xflow.model")
    validate_converter(script_file)
    if not isinstance(converter_input, list):
        raise ValueError(f"unsupported model signature {converter_input}. use ModelSignature class in xflow.model")
    else:
        for _ in converter_input:
            if not isinstance(_, ModelSignature):
                raise ValueError(f"unsupported model signature {converter_input}. "
                                 f"use ModelSignature class in xflow.model")
    if not isinstance(converter_output, list):
        raise ValueError(f"unsupported model signature {converter_output}. use ModelSignature class in xflow.model")
    else:
        for _ in converter_output:
            if not isinstance(_, ModelSignature):
                raise ValueError(f"unsupported model signature {converter_output}. "
                                 f"use ModelSignature class in xflow.model")

    xflow_client.init_check()
    client_info: xflow_client.ClientInformation = xflow_client.client_info
    url = client_info.xflow_server_url + RequestPath.deploy_export_converter
    package_list = []
    if requirements_file is not None:
        with open(requirements_file, 'r') as requirements:
            lines = requirements.readlines()
            for line in lines:
                package_list.append(line.strip())
    with open(script_file, 'r') as script_f:
        script = script_f.read()

    CNVRT_IN = []
    CNVRT_OUT = []
    for _ in converter_input:
        CNVRT_IN.append(_.dict())
    for _ in converter_output:
        CNVRT_OUT.append(_.dict())
    req_body = req_vo.ExportConverter(PRJ_ID=client_info.project,
                                      CNVRT_NM=name,
                                      CNVRT_IN=CNVRT_IN,
                                      CNVRT_OUT=CNVRT_OUT,
                                      CNVRT_BCKN=backend,
                                      CNVRT_PKG=package_list,
                                      REG_ID=client_info.user,
                                      CNVRT_NMSPC=namespace,
                                      CNVRT_SCRIPT=script)
    code, msg = req_util.post(url=url, data=req_body.dict())
    if code != 0:
        raise RuntimeError(f"failed to export converter. {msg}")
    else:
        print(f"converter {name} exported.")