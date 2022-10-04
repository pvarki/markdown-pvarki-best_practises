# Using `ssh-agent` nicely

This document is maintained at <https://gitlab.com/advian/best_practises/>

This is probably adaptable somehow to Windows but this
document will only consider UNIX-like systems.

Adapted & shortened from [this article][thearticle].

[thearticle]: https://blog.g3rt.nl/upgrade-your-ssh-keys.html

## Make sure you have ED25519 key

`ssh-keygen -o -a 100 -t ed25519`

## Legacy keys

If you need legacy RSA keys create/keep them as needed.

## ssh-agent automation

`ssh-add -l | grep -q ED25519 || ssh-add ~/.ssh/id_rsa ~/.ssh/id_rsa_legacy ~/.ssh/id_ed25519`

First query agent for keys it already knows of, then
check if your ED25519 key is loaded, if not tell the
agent to load the defined keys.

Add this line to your `~/.profile` or corresponding
(like `~/.bash_profile`).

You will need to edit the line in accordance with
the key files you actually want to use.

### WSL note

On WSL you might need to add `eval $(ssh-agent -s)` before
the `ssh-add` command to have the agent available for
you shell.

## Agent forwarding

Use `ssh -A` (or see below for editing global config)
to forward your auth agent so that you don't need to
have your keys on every intermediate machine when
connecting via jump servers or from local VMs etc.

## Global config

Edit `~/.ssh/config` and add lines

    Host *
         ServerAliveInterval 30
         ForwardAgent yes

Which basically means that for all hosts enable agent
forwarding and connection keepalive (some servers,
especially AWS ones, are very quick to drop idle connections)
