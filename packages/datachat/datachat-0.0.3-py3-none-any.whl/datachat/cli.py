import click

@click.command()
@click.argument('nome')
def main(nome):
    click.echo(f'oi {nome}')

if __name__ == '__main__':
    main()
