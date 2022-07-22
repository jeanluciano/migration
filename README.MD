# Prefect CI/CD migration

With deployments and workspaces, Orion has really the way we set up our different enviroments and deploy our flows. Today we will be migrating a basic Blue/Green deployment pipeline on prefect 1.0 to Prefect Orion.

Now with Orion, we have a new feature called deployments. Deployments have the information that 1.0 handled with run_confing. For our CI/CD  we will create two deployments in a file call deployments.py. These will specify where the flow will run, paramters for the run, tags for the flow among others. This change lets us have our information about the running and deployment of a flow seperated from the flow logic.

Another new feature that changes our flow development process is Work Queues. These pretty much do everything the RunConfig object does in 1.0; they also pick up our deployments and have them executed by either deployment ID or deployment tags i.e 'prod', 'dev'.

Lastly we have packaging. This eliminates the process of having to to create and update a requirements.txt or updating the python dependecies.  

Okay so let's migrate! First let's create our deployments, we will be creating one for each one of our enviroments. Let's give the deployments name, tags, and location of our flow. Lets also grab our schedule and flow_runner from our 1.0 flow (In 1.0 you'd have a different run_config stored using git branches).

```py
Deployment(
    name="DEV",
    tags=['dev'],
    flow_location="../flow.py",
    flow_runner= KubernetesFlowRunner(image="registry/ourdevimage"),
    schedule=IntervalSchedule(interval=timedelta(days=1)),
    packager=OrionPackager(serializer=ImportSerializer())
    
)

Deployment(
    name="PROD",
    flow_location="../flow.py",
    flow_runner= KubernetesFlowRunner(image="registry/ourprodimage"),
    tags=['prod'],
    schedule=IntervalSchedule(interval=timedelta(days=1)),
    packager=OrionPackager(serializer=ImportSerializer())
)
  
```

To create these deployments in our prefect database we type the command below in our terminal. This is the equivalent of using prefect register in the 1.0 CLI. Let's replace that line in our github actions yaml files with the following:

```sh
prefect deployment create deployments.py
```

The packager above will replace lines 13 - 16 in our github actions file. You will also never have to worry about the python dependecies of your flow!

Now, inside each respective enviroments, let's create our work queues and note their UUIDs. After that create an agent to execute our flows.

```sh
prefect work-queue create -t 'prod' prod
UUID('2607fa8f-76f0-4330-8494-6a82194205c2')

prefect agent start '2607fa8f-76f0-4330-8494-6a82194205c2'
```

```sh
prefect work-queue create -t 'dev' dev
UUID('b53e19c5-9602-48ad-9469-d75b2f83b71b')

prefect agent start 'b53e19c5-9602-48ad-9469-d75b2f83b71b'
```

Orion brings some serious QOL improvements in the CI/CD process.
Deployments and packaging allows to quickly write all the