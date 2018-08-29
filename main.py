from psutil import virtual_memory, disk_usage
import click
from slackython import Slackython

GIGABYTE = 1024 * 1024 * 1024


def default_alert(msg):
    print(msg)


def translate_to_gigabyte(size):
    return '%.3f'%(size/GIGABYTE) + 'Gb'


def check_ram(alert=default_alert, percentage=None, fixed_amount=None):
    memory = virtual_memory()
    total_memory = memory.total
    available_memory = memory.available

    if percentage:
        threshold = total_memory * percentage
    elif fixed_amount:
        threshold = fixed_amount * GIGABYTE
    else:
        threshold = GIGABYTE

    if available_memory <= threshold:
        msg = "[WARNING] LOW AVAILABLE RAM {}/{}".format(
            translate_to_gigabyte(available_memory),
            translate_to_gigabyte(total_memory)
        )
        alert(msg)


def check_disk(alert=default_alert, percentage=None, fixed_amount=None):
    disk = disk_usage('/')
    total_disk = disk.total
    available_disk = disk.free
    percentage_disk = disk.percent

    if percentage:
        must_alert = percentage_disk <= percentage
    elif fixed_amount:
        must_alert = available_disk <= fixed_amount * GIGABYTE
    else:
        must_alert = available_disk <= GIGABYTE

    if must_alert:
        msg = "[WARNING] LOW AVAILABLE DISK {}/{}".format(
            translate_to_gigabyte(available_disk),
            translate_to_gigabyte(total_disk)
        )
        alert(msg)


@click.command()
@click.option('-rp', '--ram-percentage',
              default=None, help='Percent of total ram')
@click.option('-rf', '--ram-fixed',
              default=None, help='Fixed amount of ram')
@click.option('-dp', '--disk-percentage',
              default=None, help='Percent of total disk')
@click.option('-df', '--disk-fixed',
              default=None, help='Fixed amount of disk')
@click.option('-sw', '--slack-webhook',
              default=None, help='Slack webhook')
@click.option('-sa', '--slack-admins',
              default=None, help='Slack administrator ids',
              multiple=True)
def check_system(
        ram_percentage, ram_fixed,
        disk_percentage, disk_fixed,
        slack_webhook, slack_admins
):
    """
    Program to check the system capacity on RAM and DISK and send alert if is
    lower than certain threshold set by the user.
    """
    alert = default_alert
    if slack_webhook:
        notificator = Slackython(slack_webhook, slack_admins)
        alert = lambda msg: notificator.send_error(msg, 'System Supervisor')

    check_ram(alert, ram_percentage, ram_fixed)
    check_disk(alert, disk_percentage, disk_fixed)


if __name__ == "__main__":
    check_system()
