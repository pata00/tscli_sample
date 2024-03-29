import asyncio
from tscli import AsyncTensorClient, secure_operate_pb2, packer
import define_parties
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--taskid", type=str, default="taskId",
                    help="role, defalut value is taskid")
parser.add_argument("-s", "--sub_taskid", type=str, default="subTaskId",
                    help="role, defalut value is subTaskId")
args = parser.parse_args()
print("args=", args)


async def vds_role_0_and_kill():
    arr = [1, 2, 3, 4]
    dtype = "int32"
    shape = [len(arr)]

    req = secure_operate_pb2.ExecuteRequest(
        taskId=args.taskid,
        subTaskId=args.sub_taskid,
        asyncMode=True,
        timeout=0,
        mpcProtocol=secure_operate_pb2.MpcProtocol(
            protocolCode="ss",
            providerCode="lanxiang",
            version="0.0.1",
            param={
                "aaa": "bbb"
            }
        ),
        expression="vds",
        parties=[
            define_parties.role0,
            define_parties.role1
        ],
        localPartyId=define_parties.role0,
        resultParties=[
            define_parties.role0,
            define_parties.role1
        ],
        inputs=[
            secure_operate_pb2.DataValue(
                dataValueTag=secure_operate_pb2.DataValueTag(
                    type="direct",
                    name="x",
                    dtype=dtype,
                    shape=shape
                ),
                directValue=packer.pack_to_bytes(arr, dtype)
            )
        ],
        outputMethod=[secure_operate_pb2.DataValueTag(
            type="direct"
        )],
    )

    client = AsyncTensorClient(define_parties.servring_addr0)
    resp = await client.execute(req)

    assert(resp.code == 0)

    kill_resp = await client.kill(secure_operate_pb2.TaskTabRequest(taskId=args.taskid,
                                                                    subTaskId=args.sub_taskid,  localPartyId=define_parties.role0))
    print(kill_resp)


async def main():
    await vds_role_0_and_kill()


if __name__ == "__main__":
    asyncio.run(main())
    pass
