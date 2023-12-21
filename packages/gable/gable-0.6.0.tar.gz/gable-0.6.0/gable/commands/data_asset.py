import base64
import json
import os
from typing import List, Optional, Union, cast

import click
import yaml
from click.core import Context as ClickContext
from click_option_group import optgroup
from gable.helpers.check import (
    post_data_asset_check_requests,
    post_data_assets_check_requests,
)
from gable.helpers.data_asset import (
    get_db_connection,
    get_db_schema_contents,
    get_generated_data_asset_contract,
    get_schema_contents,
    get_source_names,
    is_empty_schema_contents,
    send_schemas_to_gable,
    standardize_source_type,
    validate_db_input_args,
)
from gable.helpers.emoji import EMOJI
from gable.helpers.repo_interactions import get_git_repo_info, get_git_ssh_file_path
from gable.openapi import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetDetailedResponse,
    CheckDataAssetErrorResponse,
    CheckDataAssetNoContractResponse,
    ErrorResponse,
    ResponseType,
)
from gable.options import (
    ALL_SOURCE_TYPE_VALUES,
    DATABASE_SOURCE_TYPE_VALUES,
    FILE_SOURCE_TYPE_VALUES,
    file_source_type_options,
    global_options,
    proxy_database_options,
    required_option_callback,
)
from gable.readers.file import read_file
from loguru import logger
from rich.console import Console
from rich.table import Table

console = Console()


@click.group(name="data-asset")
def data_asset():
    """Commands for data assets"""


@data_asset.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    name="list",
)
@click.pass_context
@click.option(
    "-o",
    "--output",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Format of the output. Options are: table (default) or json",
)
@click.option(
    "--full",
    is_flag=True,
    help="Return full data asset details including namespace and name",
)
@global_options()
def list_data_assets(ctx: ClickContext, output: str, full: bool) -> None:
    """List all data assets"""
    # Get the data
    response, success, status_code = ctx.obj.client.get("v0/data-assets")

    # Format the output
    if output == "json":
        data_asset_list = []
        for data_asset in response:
            row = {"resourceName": f"{data_asset['namespace']}:{data_asset['name']}"}
            if full:
                # Filter out invalid data assets...
                if "://" in data_asset["namespace"]:
                    row["type"] = data_asset["namespace"].split("://", 1)[0]
                    row["dataSource"] = data_asset["namespace"].split("://", 1)[1]
                    row["name"] = data_asset["name"]
            data_asset_list.append(row)
        logger.info(json.dumps(data_asset_list))
    else:
        table = Table(show_header=True, title="Data Assets")
        table.add_column("resourceName")
        if full:
            table.add_column("type")
            table.add_column("dataSource")
            table.add_column("name")
        for data_asset in response:
            if not full:
                table.add_row(f"{data_asset['namespace']}:{data_asset['name']}")
            else:
                # Filter out invalid data assets...
                if "://" in data_asset["namespace"]:
                    table.add_row(
                        f"{data_asset['namespace']}:{data_asset['name']}",
                        data_asset["namespace"].split("://", 1)[0],
                        data_asset["namespace"].split("://", 1)[1],
                        data_asset["name"],
                    )
        console.print(table)


@data_asset.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    name="register",
    epilog="""Example:

gable data-asset register --source-type postgres \\
    --host prod.pg.db.host --port 5432 --db transit --schema public --table routes \\
    --proxy-host localhost --proxy-port 5432 --proxy-user root --proxy-password password""",
)
@click.pass_context
@click.option(
    "--source-type",
    callback=required_option_callback,
    is_eager=True,
    type=click.Choice(list(ALL_SOURCE_TYPE_VALUES), case_sensitive=True),
    help="""The type of data asset.
    
    For databases (postgres, mysql) a data asset is a table within the database.

    For protobuf/avro/json_schema a data asset is message/record/schema within a file.
    """,
)
@proxy_database_options(
    option_group_help_text="""Options for registering database tables as data assets. Gable relies on having a proxy database that mirrors your 
    production database, and will connect to the proxy database to register tables as data assets. This is to ensure that 
    Gable does not have access to your production data, or impact the performance of your production database in any way. 
    The proxy database can be a local Docker container, a Docker container that is spun up in your CI/CD workflow, or a
    database instance in a test/staging environment. The tables in the proxy database must have the same schema as your 
    production database for all tables to be correctly registered. The proxy database must be accessible from the 
    machine that you are running the gable CLI from.

    If you're registering tables in your CI/CD workflow, it's important to only register from the main branch, otherwise 
    you may end up registering tables that do not end up in production.
    """,
    action="register",
)
@file_source_type_options(
    option_group_help_text="""Options for registering a Protobuf message, Avro record, or JSON schema object as data assets. These objects 
    represent data your production services produce, regardless of the transport mechanism. 

    If you're registering Protobuf messages, Avro records, or JSON schema objects in your CI/CD workflow, it's important 
    to only register from the main branch, otherwise you may end up registering records that do not end up in production.
    """,
    action="register",
)
@global_options()
def register_data_asset(
    ctx: ClickContext,
    source_type: str,
    host: str,
    port: int,
    db: str,
    schema: str,
    table: Union[str, None],
    proxy_host: str,
    proxy_port: int,
    proxy_db: str,
    proxy_schema: str,
    proxy_user: str,
    proxy_password: str,
    files: tuple,
) -> None:
    """Registers a data asset with Gable"""
    # Standardize the source type
    source_type = standardize_source_type(source_type)
    tables: list[str] | None = [t.strip() for t in table.split(",")] if table else None
    if source_type in DATABASE_SOURCE_TYPE_VALUES:
        proxy_db = proxy_db if proxy_db else db
        proxy_schema = proxy_schema if proxy_schema else schema
        files_list: list[str] = []
    else:
        # Turn the files tuple into a list
        files_list: list[str] = list(files)
    # This won't be set for file-based data assets, but we need to pass through
    # the real db.schema value in case the proxy database has different names
    database_schema = ""

    source_names: list[str] = []
    schema_contents: list[str] = []
    # Validate the source type arguments and get schema contents
    if source_type in DATABASE_SOURCE_TYPE_VALUES:
        validate_db_input_args(proxy_user, proxy_password, proxy_db)
        connection = get_db_connection(
            source_type, proxy_user, proxy_password, proxy_db, proxy_host, proxy_port
        )
        schema_contents.append(
            json.dumps(
                get_db_schema_contents(connection, proxy_schema, tables=tables or None)
            )
        )

        database_schema = f"{db}.{schema}"
        source_names.append(f"{host}:{port}")
    elif source_type in FILE_SOURCE_TYPE_VALUES:
        for file in files_list:
            schema_contents.append(read_file(file))
            with logger.contextualize(context=file):
                git_file_path = get_git_ssh_file_path(get_git_repo_info(file), file)
                logger.trace(f"Git file path: {git_file_path}")
                source_names.append(git_file_path)
    else:
        raise NotImplementedError(f"Unknown source type: {source_type}")
    if is_empty_schema_contents(source_type, schema_contents):
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found found to register! You can use the --debug or --trace flags for more details."
        )
    # Send the schemas to Gable
    response, success, status_code = send_schemas_to_gable(
        ctx.obj.client, source_type, source_names, database_schema, schema_contents
    )
    if not success:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} Registration failed for some data assets: {str(response)}"
        )
    logger.info(
        f"{EMOJI.GREEN_CHECK.value} Registration successful: {response['registered']}"
    )


@data_asset.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    name="check",
    epilog="""Example:

gable data-asset check --source-type protobuf --files ./**/*.proto""",
)
@click.pass_context
@click.option(
    "--source-type",
    required=True,
    type=click.Choice(ALL_SOURCE_TYPE_VALUES, case_sensitive=True),
    help="""The type of data asset.
    
    For databases (postgres, mysql) the check will be performed for all tables within the database.

    For protobuf/avro/json_schema the check will be performed for all file(s)
    """,
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["text", "json", "markdown"]),
    default="text",
    help="Format of the output. Options are: text (default), json, or markdown which is intended to be used as a PR comment",
)
@proxy_database_options(
    option_group_help_text="""Options for checking contract compliance for tables in a relational database. The check will be performed
    for any tables that have a contract associated with them.
    
    Gable relies on having a proxy database that mirrors your production database, and will connect to the proxy database
    to perform the check in order to perform the check as part of the CI/CD process before potential changes in the PR are
    merged.
    """,
    action="check",
)
@file_source_type_options(
    option_group_help_text="""Options for checking Protobuf message(s), Avro record(s), or JSON schema object(s)for contract violations.""",
    action="check",
)
@global_options()
def check_data_asset(
    ctx: ClickContext,
    source_type: str,
    output: str,
    host: str,
    port: int,
    db: str,
    schema: str,
    table: str,
    proxy_host: str,
    proxy_port: int,
    proxy_db: str,
    proxy_schema: str,
    proxy_user: str,
    proxy_password: str,
    files: tuple,
) -> None:
    """Checks data asset(s) against a contract"""
    # Standardize the source type
    source_type = standardize_source_type(source_type)
    tables: list[str] | None = [t.strip() for t in table.split(",")] if table else None
    if source_type in DATABASE_SOURCE_TYPE_VALUES:
        proxy_db = proxy_db if proxy_db else db
        proxy_schema = proxy_schema if proxy_schema else schema
        files_list: list[str] = []
    else:
        # Turn the files tuple into a list
        files_list: list[str] = list(files)
    schema_contents = get_schema_contents(
        source_type=source_type,
        dbuser=proxy_user,
        dbpassword=proxy_password,
        db=proxy_db,
        dbhost=proxy_host,
        dbport=proxy_port,
        schema=proxy_schema if proxy_schema else schema,
        tables=tables,
        files=files_list,
    )
    source_names = get_source_names(
        ctx=ctx,
        source_type=source_type,
        dbhost=host,
        dbport=port,
        files=files_list,
    )

    if is_empty_schema_contents(source_type, schema_contents):
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found found to check! You can use the --debug or --trace flags for more details."
        )

    if output == "text":
        # Legacy behavior
        results = post_data_asset_check_requests(
            ctx.obj.client, source_type, source_names, db, schema, schema_contents
        )
        results_string = "\n".join(
            [  # For valid contracts, just print the check mark and name
                f"{EMOJI.GREEN_CHECK.value} {name}" if result[1] == 200 else
                # For missing contracts print a warning
                f"{EMOJI.YELLOW_WARNING.value} {name}:\n\t{result[0]}"
                if result[1] == 404
                else
                # For invalid contracts, print the check results
                f"{EMOJI.RED_X.value} {name}:\n\t{result[0]}"
                for name, result in results.items()
            ]
        )
        # 404s are "OK", treat them as warnings
        if min(map(lambda x: x[1] == 200 or x[1] == 404, results.values())) == False:
            raise click.ClickException(
                f"\n{results_string}\nContract violation(s) found"
            )
        else:
            logger.info(results_string)
            logger.info("No contract violations found")
    else:
        response_type = (
            ResponseType.COMMENT_MARKDOWN
            if output == "markdown"
            else ResponseType.DETAILED
        )
        results = post_data_assets_check_requests(
            ctx.obj.client,
            response_type,
            source_type,
            source_names,
            db,
            schema,
            schema_contents,
        )
        if type(results) == ErrorResponse:
            raise click.ClickException(results.message)
        if response_type == ResponseType.COMMENT_MARKDOWN:
            results = cast(CheckDataAssetCommentMarkdownResponse, results)
            # Only echo the markdown if it's not None or empty, otherwise the stdout will contain a newline
            if results.markdown and results.markdown != "":
                logger.info(results.markdown)
            # Raise an exception if there were errors
            if results.errors:
                errors_string = "\n".join(
                    [json.dumps(error.dict()) for error in results.errors]
                )
                raise click.ClickException(
                    f"{EMOJI.RED_X.value} Contract checking failed for some data assets:\n{errors_string}"
                )
        else:
            results = cast(
                list[
                    CheckDataAssetDetailedResponse
                    | CheckDataAssetErrorResponse
                    | CheckDataAssetNoContractResponse
                ],
                results,
            )
            # Convert the results to dicts by calling Pydantic's json() on each result to deal with enums, which
            # aren't serializable by default
            results_dict = [json.loads(result.json()) for result in results]
            # Check if there were any errors to determine whether to just echo the results or raise an exception
            if any([type(result) == CheckDataAssetErrorResponse for result in results]):
                raise click.ClickException(
                    json.dumps(results_dict, indent=4, sort_keys=True)
                )
            logger.info(json.dumps(results_dict, indent=4, sort_keys=True))


@data_asset.command(
    name="create-contract",
    epilog="""Example:
                    
gable data-asset create-contract --data-asset-id postgres://sample.host:5432:db.public.table --output-dir contracts""",
)
@click.pass_context
@click.argument(
    "data_asset_ids",
    nargs=-1,
)
@click.option(
    "--output-dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    help="Directory to output contracts. This directory must exist",
)
def create_data_asset_contracts(
    ctx: ClickContext, data_asset_ids: List[str], output_dir: Optional[str]
) -> None:
    """Creates the YAML contract specification for a list of data assets

    The specification that is produced is based off the registered data asset but the
    user will need to fill in places marked with 'FIX:' such as field descriptions and
    ownership information.
    """
    for data_asset_id in data_asset_ids:
        logger.debug(f"Creating contract for data asset: {data_asset_id}")

        # Base64 encode the data asset ID
        encoded_resource_name = base64.b64encode(data_asset_id.encode("utf-8")).decode(
            "utf-8"
        )

        # Get the inferred contract for the data asset
        response, success, status_code = get_generated_data_asset_contract(
            ctx.obj.client, encoded_resource_name
        )
        if not success:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Failed to generate contract for data asset: {data_asset_id} ({status_code}))"
            )

        # Get the raw contract spec and convert to yaml
        contract_spec_dict = json.loads(response["contractSpecRaw"])
        contract_spec_yaml = yaml.dump(
            contract_spec_dict, default_flow_style=False, sort_keys=False
        )

        # Print out the data asset
        logger.info(contract_spec_yaml)

        if output_dir:
            # Get the contract name for the filename
            name = response["contractSpec"]["name"].lower().replace(".", "_")
            filepath = os.path.join(output_dir, f"{name}.yaml")

            # Write the contract spec to a file
            with open(filepath, "w") as f:
                f.write(contract_spec_yaml)
