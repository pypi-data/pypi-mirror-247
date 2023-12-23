import click
import time


@click.group()
def cli():
    pass


@click.command()
@click.option('--name', prompt='Identify youself by name')
def greet(name):
    """Describe this tool with colors to You."""
    click.secho(f"Hello {name}", bold=True, bg='green', fg='black')
    click.secho(
        "This is Command Line Interface which gives information of maker named Piyush.", bg='blue', fg='white')


@click.command()
@click.option('--desc', default=False, show_default=True, help='Show detailed Info.')
def bio(desc):
    """Basic Bio"""
    if desc:
        click.echo("Hey, this is piyush here, thanks for your interest.\nTo know more about me please run this CLI and different commands.\nThank You!")
    else:
        click.echo("This is me, and describing self.")


@click.command()
def age():
    """Get Age"""
    click.echo("I'm 2X years older, shouldn't be matter.")


@click.command()
def skills():
    """Get my dummy skills set with progress bar"""
    skill_set = ["JavaScript", "Python", "GraphQL", "C", "TypeScript", "VueJS",
                 "NuxtJS", "Socket Programming", "Machine Learning", "NodeJS", "Linux"]

    with click.progressbar(skill_set, label='Getting skills', length=len(skill_set)-1, show_eta=False, color='blue') as skill_list:
        for skill in skill_list:
            click.echo(f" {skill}")
            time.sleep(0.3)


@click.command()
def blog():
    """Get My blog URL"""
    blog_url = "https://blog.thesourcepedia.org/"
    click.echo(f"{blog_url}   Wanna visit [y/n]: ", nl=False)
    c = click.getchar()
    click.echo(c)
    if c == 'y':
        click.echo("Launching Piyush's Blog")
        click.launch(blog_url)


@click.command()
def portfolio():
    """Launch my Portfolio!"""
    click.launch("https://github.com/daflongustavo/")


# @click.command()
# @click.Choice()
cli.add_command(greet)
cli.add_command(bio)
cli.add_command(age)
cli.add_command(skills)
cli.add_command(blog)
cli.add_command(portfolio)

if __name__ == '__main__':
    cli()
