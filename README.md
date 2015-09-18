# qstate
`qstate` is a multi-container state-queue-as-a-service web API.  It's build on the following technology:
* [Python](https://www.python.org/) (business logic)
* [Docker](https://www.docker.com/) (containerization)
* [Gearman](http://gearman.org) (scalability and job management)
* [Redis](http://redis.io/) (storage)

## Architecture

The `qstate` component is designed to manage global state for a distributed API architecture.  Its design is extremely simple:

1. It maintains a queue of states, denoted simply by simple strings.
2. When the queue is incremented/moves to the next state, the state queue fires a message to all attached components via an API adapter.

Limitations:
1. The `qstate` queue is one-directional, and once a state is moved past it cannot be revisited.
2. `qstate` does not store anything functional about states: it simple stores their string identifiers.

The two components of `qstate`, the API interface and the state publisher are connected through a gearman container.

## Installation

Installation assumes that you already have Docker and its prerequisites installed.  See [Docker Docs](https://docs.docker.com/).  The best and easiest way to install is through Docker Compose.

1. Clone the repository:
<pre>
$ git clone https://github.com/christhebrews/qstate
$ cd qstate/
</pre>

2. Build docker images with Docker Compose:
<pre>$ docker-compose build</pre>

3. Start the containers with Docker Compose:
<pre>$ docker-compose up -d</pre>

4. Get the IP of your docker machine:
<pre>
$ docker-machine active
MY_ACTIVE_MACHINE
$ docker-machine ip MY_ACTIVE_MACHINE
</pre>

5. Point your browser to the IP address on port 80 to get to the qstate debug screen.
 
## API

The following API endpoints are exposed in `qstate`:

#### POST /push
Post a new state onto the end of the queue.

_Request:_
<pre>
{
  "state": string
}
</pre>

_Response:_
<pre>
{
  "success": true
}
</pre>

#### POST /next
Iterate the queue to the next active state.  If no queued states remain, the active state is set to null.

_Response:_
<pre>
{
  "active_state": "state"
}
</pre>

#### GET /state
Get the current active state in the queue.  If there is no valid active state, null is returned.

_Response:_
<pre>
{
  "active_state": "state"
}
</pre>

#### GET /debug
Get debug data for the queue.

_Response:_
<pre>
{
  "active_state": "state"
  "queue": []
}
</pre>

#### State Update Trigger
`qstate` will trigger a REST call to any connected adapters on state change (see Configuration) with the following payload:
<pre>
{
  "state": string
}
</pre>

## Configuration
`qstate` allows for the setup of multiple separate configurations in the conf/ directory.  Each configuration file should be named according to the `APP_MODE` environment variable in the `docker-compose.yml` file.

For instance, if you set the `APP_MODE=prod`, `qstate` will use the `conf/prod.json` configuration file.

Configuration sample:
<pre>
{
    "redis": {
        "host": "redis",
        "port": 6379,
        "db": 1
    },
    "adapters": [
        {
            "name": "local_server",
            "url": "http://localhost/updateState.php"
        }, {
            "name": "remote_server",
            "url": "http://192.169.56.101/changeState/"
        }
    ],
    "gearman": {
        "job_server": "gearman:4730",
        "job_prefix": "statequeue-"
    }
}
</pre>

#### Redis

Redis configuration.

* `host` (string): hostname of the redis server, by default this is just "redis" because this is the name of the linked container in docker-compose
* `port` (int): the port redis uses (make sure that the `docker-compose.yml` file exposes this port)
* `db` (int): Database id to use

#### Adapters

Attached adapters for components

You can specify as many adapters as you like here, each adapter just needs two things:
* `name` (string): a human-readable name for your adapter
* `url` (string): the URL endpoint that can recieve the state update trigger payload and update the state for that component

#### Gearman

Gearman config.

* `job_server` (string): this should be the gearman job server and port in the format hostname:port.  Note that the hostname is "gearman" because this is the name of the linked container in docker-compose.  The port is exposed as well.
* `job_prefix` (string): a prefix for `qstate` gearman jobs, in case you're using the same gearman server for multiple services (why not, right?)
