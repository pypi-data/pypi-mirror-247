import argh
from scale_egp.egpcli.collections import (
    CollectionCRUDCommands,
    EGPClientFactory,
    ModelAliasCRUDCommands,
    ModelTemplateCRUDCommands,
)


def add_crud_commands_to_parser(
    parser: argh.ArghParser, name: str, commands: CollectionCRUDCommands
):
    parser.add_commands([commands.create, commands.get], group_name=name)


def exec_cli():
    client_factory = EGPClientFactory()

    parser = argh.ArghParser()
    parser.add_argument("-a", "--api-key", type=str, default=None)
    parser.add_argument("-e", "--endpoint-url", type=str, default=None)
    model_alias_commands = ModelAliasCRUDCommands(client_factory)
    parser.add_commands(
        [model_alias_commands.create, model_alias_commands.get, model_alias_commands.execute],
        group_name="model",
    )
    add_crud_commands_to_parser(parser, "model_template", ModelTemplateCRUDCommands(client_factory))
    args = parser.parse_args()
    client_factory.set_client(api_key=args.api_key, endpoint_url=args.endpoint_url)
    parser.dispatch()
