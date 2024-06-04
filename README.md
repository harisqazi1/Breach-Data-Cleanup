Breach Data Cleanup
===================

A set of scripts to cleanup breach data (including combo-lists and
stealer logs) to normalized formats (CSV and JSON) that can be used with
indexing solutions. The languages will primarily be Python and Bash.

**Please compare the information of your breach to the one in this repo to make sure the breaches are the same. It is completely possible for me to have limited or incorrect data.**

This is a work in progress. In addition, I can only include scripts for
breaches that ***I have access to***. If you want to request a script
for a breach that I don't have, you will also have to share the link to
the breach as well.

Testing Environment
-------------------

I am using Apache Solr containerized as my testing environment. Why
Solr? It is well built tool and I do enjoy its simplicity. It is also
open source (https://github.com/apache/solr). Using Solr in a container
makes cleanup really easy. I use Podman really for one main reason: it
executes commands directly and avoids the need for root privileges. If
you want to replicate my test environment, see the following:

### Install Podman:

`sudo apt -y install podman`

### Pull Solr from the Docker repository:

`podman pull docker.io/solr`

### Creating a container called solr\_breach:

`podman run -d -p 8983:8983 --name solr_breach solr`

> -d = Run container in background and print container ID

> -p = Publish a container's port, or a range of ports, to the host (default \[\])

> --name = Assign a name to the container

### Check to see if container is running:

`podman container list`

**At this point, if container is running, Solr**

### Create a breach core:

`podman exec -it solr_breach bin/solr create_core -c breach`

> -i, --interactive Keep STDIN open even if not attached

> -t, --tty Allocate a pseudo-TTY. The default is false

> -it = --interactive + --tty

> bin/solr = program on the container to run

> create\_core -c breach = create a core named "breach"

NOTE:
`podman run -d -p 8983:8983 --name my_solr solr solr-precreate gettingstarted`
\#could be used as well

### Make a directory you will connect to the container.

NOTE: This will be to transfer breaches from your local directory to the
container directory.

`mkdir solr_local`

### Post (send) the data to Solr

NOTE: (I ran this in directory where I had file; \$PWD =
"/home/\[user\]/Downloads/solr\_local")

`podman run --rm -v "$PWD:/mydata" --network=host solr bin/solr post -c breach /mydata/soletrade-users.txt.json`

> --rm Remove container (and pod if created) after exit

> -v, --volume stringArray Bind mount a volume into the container

> --network string Connect a container to a network

> bin/solr post -c breach /mydata/soletrade-users.txt.json = post the .json file to the breach core

NOTE: Podman/Docker uses volumes as
"local\_directory:container\_directory". Mentioned to clarify why
"/mydata/" was used here in command.

At this point you are where you need to be to test. The following are
informational:

### Remove container

`podman stop solr_breach`

`podman rm solr_breach`

### Restart container after stopping it

`podman start solr_breach`

### Deleting all documents in a core

-   Go to `http://0.0.0.0:8983/solr/#/breach/documents`
-   change document type to XML
-   Add the following under `Document(s)`:

```XML
<delete> 
   <query>*:*</query> 
</delete>
```

-   Hit Submit Button
