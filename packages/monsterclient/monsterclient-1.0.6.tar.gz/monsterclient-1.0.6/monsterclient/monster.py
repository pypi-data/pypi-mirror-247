import click
from monsterclient.api import MonsterAPI, AuthAPI, TokenV1, TokenV3

monsterAPI = MonsterAPI()
authAPI = AuthAPI()


@click.command(help="GET a new token")
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
@click.option("-v", "--version", help="auth version")
def token(curl, version):
    if version == "3":
        token = TokenV3()
    elif version == "1" or version == None:
        token = TokenV1()

    response = authAPI.write_monster_connection(token)
    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="PUT container | object")
@click.argument("container")
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def put(container, obj, curl):
    if obj:
        response = monsterAPI.upload_object(container, obj)
    else:
        response = monsterAPI.create_container(container)

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="DELETE container | object")
@click.argument("container")
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def delete(container, obj, curl):
    if obj:
        response = monsterAPI.delete_object(container, obj)
    else:
        response = monsterAPI.delete_container(container)

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="HEAD container | object | account")
@click.argument("container", required=False)
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def head(container, obj, curl):
    if obj and container:
        response = monsterAPI.head_object(container, obj)
    elif not obj and container:
        response = monsterAPI.head_container(container)
    else:
        response = monsterAPI.head_account()

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="GET container | object | account")
@click.argument("container", required=False)
@click.argument("obj", required=False)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def get(container, obj, curl):
    if obj and container:
        response = monsterAPI.get_object(container, obj)
    elif not obj and container:
        response = monsterAPI.get_container(container)
    else:
        response = monsterAPI.get_account()

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="POST container | object | account")
@click.argument("container", required=False)
@click.argument("obj", required=False)
@click.option(
    "-H",
    "--header",
    help="for set metadata use: x-account/container/object-meta-key:value",
)
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def post(container, obj, header, curl):
    if obj and container:
        response = monsterAPI.post_object(container, obj, header)
    elif not obj and container:
        response = monsterAPI.post_container(container, header)
    else:
        response = monsterAPI.post_account(header)

    click.echo(f"{response.repr(curl=curl)}")


@click.command(help="Get info")
@click.option("-c", "--curl", is_flag=True, help="print curl command if specified")
def info(curl):
    response = monsterAPI.get_info()
    click.echo(f"{response.repr(curl=curl)}")


@click.group(help="CLI tool for Monster")
def main():
    pass


main.add_command(token)
main.add_command(put)
main.add_command(delete)
main.add_command(head)
main.add_command(get)
main.add_command(post)
main.add_command(info)

if __name__ == "__main__":
    main()
