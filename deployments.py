from prefect.deployments import Deployment
from prefect.flow_runners import SubprocessFlowRunner

Deployment(
    name="DEV",
    flow_location="../flow.py",
    flow_runner= SubprocessFlowRunner( stream_output=True),
    tags=['dev'],
    
)

Deployment(
    name="PROD",
    flow_location="../flow.py",
    flow_runner= SubprocessFlowRunner(),
    tags=['prod'],
    
)
  
  