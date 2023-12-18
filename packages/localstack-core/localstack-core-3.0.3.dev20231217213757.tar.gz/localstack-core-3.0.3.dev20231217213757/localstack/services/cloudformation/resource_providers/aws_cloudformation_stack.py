# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class CloudFormationStackProperties(TypedDict):
    TemplateURL: Optional[str]
    Id: Optional[str]
    NotificationARNs: Optional[list[str]]
    Parameters: Optional[dict]
    Tags: Optional[list[Tag]]
    TimeoutInMinutes: Optional[int]


class Tag(TypedDict):
    Key: Optional[str]
    Value: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class CloudFormationStackProvider(ResourceProvider[CloudFormationStackProperties]):
    TYPE = "AWS::CloudFormation::Stack"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[CloudFormationStackProperties],
    ) -> ProgressEvent[CloudFormationStackProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - TemplateURL



        Read-only properties:
          - /properties/Id



        """
        model = request.desired_state

        # TODO: validations

        if not request.custom_context.get(REPEATED_INVOCATION):
            if not model.get("StackName"):
                model["StackName"] = util.generate_default_name(
                    request.stack_id, request.logical_resource_id
                )

            create_params = util.select_attributes(
                model,
                [
                    "StackName",
                    "Parameters",
                    "NotificationARNs",
                    "TemplateURL",
                    "TimeoutInMinutes",
                    "Tags",
                ],
            )

            create_params["Capabilities"] = [
                "CAPABILITY_IAM",
                "CAPABILITY_NAMED_IAM",
                "CAPABILITY_AUTO_EXPAND",
            ]

            create_params["Parameters"] = [
                {
                    "ParameterKey": k,
                    "ParameterValue": str(v).lower() if isinstance(v, bool) else str(v),
                }
                for k, v in create_params.get("Parameters", {}).items()
            ]

            result = request.aws_client_factory.cloudformation.create_stack(**create_params)
            model["Id"] = result["StackId"]

            request.custom_context[REPEATED_INVOCATION] = True
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        stack = request.aws_client_factory.cloudformation.describe_stacks(StackName=model["Id"])[
            "Stacks"
        ][0]
        model["Outputs"] = {o["OutputKey"]: o["OutputValue"] for o in stack.get("Outputs", [])}
        match stack["StackStatus"]:
            case "CREATE_COMPLETE":
                return ProgressEvent(
                    status=OperationStatus.SUCCESS,
                    resource_model=model,
                    custom_context=request.custom_context,
                )
            case "CREATE_IN_PROGRESS":
                return ProgressEvent(
                    status=OperationStatus.IN_PROGRESS,
                    resource_model=model,
                    custom_context=request.custom_context,
                )
            case "CREATE_FAILED":
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resource_model=model,
                    custom_context=request.custom_context,
                )
            case _:
                raise Exception(f"Unexpected status: {stack['StackStatus']}")

    def read(
        self,
        request: ResourceRequest[CloudFormationStackProperties],
    ) -> ProgressEvent[CloudFormationStackProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[CloudFormationStackProperties],
    ) -> ProgressEvent[CloudFormationStackProperties]:
        """
        Delete a resource
        """

        model = request.desired_state
        if not request.custom_context.get(REPEATED_INVOCATION):
            request.aws_client_factory.cloudformation.delete_stack(StackName=model["Id"])

            request.custom_context[REPEATED_INVOCATION] = True
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        try:
            stack = request.aws_client_factory.cloudformation.describe_stacks(
                StackName=model["Id"]
            )["Stacks"][0]
        except Exception as e:
            if "does not exist" in str(e):
                return ProgressEvent(
                    status=OperationStatus.SUCCESS,
                    resource_model=model,
                    custom_context=request.custom_context,
                )
            raise e

        match stack["StackStatus"]:
            case "DELETE_COMPLETE":
                return ProgressEvent(
                    status=OperationStatus.SUCCESS,
                    resource_model=model,
                    custom_context=request.custom_context,
                )
            case "DELETE_IN_PROGRESS":
                return ProgressEvent(
                    status=OperationStatus.IN_PROGRESS,
                    resource_model=model,
                    custom_context=request.custom_context,
                )
            case "DELETE_FAILED":
                return ProgressEvent(
                    status=OperationStatus.FAILED,
                    resource_model=model,
                    custom_context=request.custom_context,
                )
            case _:
                raise Exception(f"Unexpected status: {stack['StackStatus']}")

    def update(
        self,
        request: ResourceRequest[CloudFormationStackProperties],
    ) -> ProgressEvent[CloudFormationStackProperties]:
        """
        Update a resource


        """
        raise NotImplementedError
