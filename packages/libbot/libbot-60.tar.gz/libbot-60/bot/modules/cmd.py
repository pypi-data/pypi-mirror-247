# This file is placed in the Public Domain.
#
# pylint: disable=C0116,E0402,E0401,W0105


"list of commands"


from bot import Commands


def cmd(event):
    event.reply(",".join(sorted(Commands.cmds)))
