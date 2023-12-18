import asyncio
from typing import Optional, List
from enum import Enum
import requests
import json
import websockets


class JobFailed(Exception):
    def __init__(self, message="Skymap Job Processing Job Failed"):
        super().__init__(message)

def snake_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])

def convert_keys_to_camel_case(dictionary):
    if isinstance(dictionary, dict):
        new_dict = {}
        for key, value in dictionary.items():
            new_key = snake_to_camel(key)
            new_value = convert_keys_to_camel_case(value) if isinstance(value, (dict, list)) else value
            new_dict[new_key] = new_value
        return new_dict
    elif isinstance(dictionary, list):
        return [convert_keys_to_camel_case(item) for item in dictionary]
    else:
        return dictionary

class KeyValuePair():
    def __init__(self, name:str, value:str) -> None:
        self.name = name
        self.value = value

class ResourceType(Enum):
    GPU = "GPU"
    MEMORY = "MEMORY"
    VCPU = "VCPU"

class FileType(Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"

class ResultType(Enum):
    RASTER = "RASTER"
    VECTOR = "VECTOR"

class ResourceRequirement():
    def __init__(self, value: str, type: ResourceType) -> None:
        self.type = type
        self.value = value

class JobConfig():
    def __init__(self, definition:str, queue_name:str, command:List[str]=[], environment:List[KeyValuePair]=[], resource_requirements:List[ResourceRequirement]=[]):
        self.definition = definition
        self.queue_name = queue_name
        self.resource_requirements = resource_requirements
        self.command = command
        self.environment = environment

class ProcessingInput():
    def __init__(self,name: str, source: str,destination: str, type: FileType, processor:Optional[JobConfig] = None):
        self.name = name
        self.source = source
        self.destination = destination
        self.type = type
        self.processor = processor

class Result():
    def __init__(self, type:ResourceType, destination:Optional[str]=None) -> None:
        self.type = type
        self.destination = destination

class ProcessingInput():
    def __init__(self,name: str, source: str,destination: str, type: str, processor:Optional[JobConfig] = None):
        self.name = name
        self.source = source
        self.destination = destination
        self.type = type
        self.processor = processor

class ProcessingOutput(ProcessingInput):
    def __init__(self, name: str, source: str, destination: str, type: FileType, processor: JobConfig | None = None, result:Optional[Result]=None):
        super().__init__(name, source, destination, type, processor)
        self.result = result

class Credential():
    def __init__(self, endpoint:str,ws_endpoint:str,secret_key:str, region:str):
        self.secret_key = secret_key
        self.region = region
        self.endpoint = endpoint
        self.ws_endpoint = ws_endpoint

class Processor(object):
    def __init__(self, 
        credential: Credential, 
        name: str, 
        main_job: JobConfig,
        is_persistent_storage: bool = False,
        storage_id: Optional[str] = None,
        processing_inputs: List[ProcessingInput] = [], 
        processing_outputs:List[ProcessingOutput] = [],
        execution_id = None
    ):
    
        self.credential = credential
        self.name = name
        self.main_job = main_job
        self.is_persistent_storage = is_persistent_storage
        self.storage_id = storage_id
        self.processing_inputs = processing_inputs 
        self.processing_outputs = processing_outputs
        self.region = self.credential.region
        self.execution_id = execution_id

    def to_dict(self):
        dict = json.loads(json.dumps(self, default=lambda o: o.__dict__))
        del dict["credential"]
        del dict["execution_id"]
        return convert_keys_to_camel_case(dict)

    async def wait(self):
        headers = [
            ("x-secret-key", self.credential.secret_key),
            ("execution-id", self.execution_id),
        ]
        try:
            async with websockets.connect(self.credential.ws_endpoint, extra_headers=headers) as websocket:
                print("Connected to Skymap Job Procesing Network")
                print(f"Execution ID: {self.execution_id}")
                while True:
                    message = await websocket.recv()
                    print(message)
                    if message == "EXECUTION_FAILED" or message == "EXECUTION_SUCCEEDED":
                        await websocket.close()
                        if message == "EXECUTION_FAILED":
                            raise JobFailed()
        except websockets.ConnectionClosed as e:
            print(f"Connection closed")
        except JobFailed as e:
            raise e

    def run(self, wait:bool= True):
        if(self.execution_id is None):
            headers = {"x-secret-key": self.credential.secret_key}
            data = requests.post(f"{self.credential.endpoint}/api/executions", json=self.to_dict(),headers=headers)
            print("Job created successfully!")
            data = data.json()["data"]
            self.execution_id = data["id"]
            requests.post(f"{self.credential.endpoint}/api/executions/{self.execution_id}/start", headers=headers)
            print("Start processing job.............")
        if(wait):
            asyncio.get_event_loop().run_until_complete(self.wait())
       
if __name__ == "__main__":
    processing_inputs = [
        ProcessingInput(
            name="input-1", 
            source="s3://skymap-datahub-prod/orders/024dd898-9aa4-42bf-beff-cf7221fafe21/mosaic_all_10m.tif",
            destination= "/data/mosaic_all_10m.tif",
            type=FileType.FILE.value
        )
    ]
    processing_outputs = [
        ProcessingOutput(
            name="output-1", 
            source="/data/super_resolution_x10.tif",
            destination= "s3://skymap-datahub/test/super_resolution_x10.tif",
            type=FileType.FILE.value
        )
    ]

    main_job = JobConfig(
        definition ="SuperResolutionJobDef",
        queue_name = "GpuSpotJobQueue",
        environment = [
            KeyValuePair("INPUT_PATH","/data/mosaic_all_10m.tif"),
            KeyValuePair("OUTPUT_PATH","/data/super_resolution_x10.tif")
        ]
    )

    processor = Processor(
        credential=Credential(
            endpoint="https://smzmn4uxvn2mplksckvqxn22ki0dalut.lambda-url.ap-southeast-1.on.aws",
            secret_key="sk_797a7693186b0C22873BBc097396B5bBB7b4eE50",
            region="us-west-2",
            ws_endpoint="wss://ppkp6aeky4.execute-api.ap-southeast-1.amazonaws.com/dev"
        ),
        name= "Job1",
        main_job=main_job,
        is_persistent_storage=False,
        processing_inputs=processing_inputs,
        processing_outputs=processing_outputs,
    )
    processor.run()

    print("Job succeeded. Do something here")

