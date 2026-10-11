# Logging

All applications we produce MUST output their logs in [ECS][ECS] compatible [ndJSON][ndjson] format by default.
They MAY additionally have ENV variable support for changing to a format that developers consider better for local
development.

[ECS]: https://www.elastic.co/guide/en/ecs/current/index.html
[ndjson]: https://github.com/ndjson/ndjson-spec

You can use https://github.com/trentm/go-ecslog to pretty-print the ECS logs.

## Python

https://github.com/pvarki/python-libpvarki provides easy logging init that you can use to achieve the requirements.

Log through a module-level `LOGGER = logging.getLogger(__name__)` at the right level, tests included; never use
`print()` for logging or debugging. A CLI's actual output goes through its CLI framework (e.g. `click.echo`).

Elastic also provides package called [ecs-logging][ecs-logging] if for some reason you cannot use the common init.

[ecs-logging]: https://www.elastic.co/guide/en/ecs-logging/python/current/installation.html

## Node

Until we have libpvarki for JS you can use [Elastic provided formatters][ecs-node] to format outputs from
popular loggers to be ECS compatible.

[ecs-node]: https://www.elastic.co/guide/en/ecs-logging/nodejs/current/intro.html

## Audit

Log security events (authentication or authorization failures, denied downloads, expired or invalid tokens and links,
privilege changes) at libpvarki's AUDIT level (`add_trace_and_audit()`). Default the actor from the authenticated
request context (client certificate or token), not from values assembled at each call site.
