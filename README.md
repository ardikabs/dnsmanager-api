# DNS Manager API Server
This is DNS Manager API Server, built with Flask & dnspython package. You can manager your DNS Zone record with this API with simply using keyring variable.

### Prerequisite
* DNS Basic Knowledge (BIND9)
* Python Knowledge
* Docker Knowledge

## Usage
Base URL: `/api/v1/`

### Endpoint
* `/zones/` - Used for manage DNS Zone, method available are:
    * `[GET]`
    * `[POST]`
    * `[PUT]`
    * `[DELETE]`
* `/records/` - Used for manage Record that registered on DNS Zone, method available are:
    * `[GET]`
    * `[POST]`
    * `[PUT]`
    * `[DELETE]`

### Setup Local Deployment
* Go over in `/project` - Project Directory
* `pip install -r requirements.txt` - Installing Dependency
* `python manage.py recreatedb` - Setup Local Database (make sure change your database default database will using data-dev.db)
* Before running the Server, make sure you just create an environment variable in `.env` file
* `python manage.py run` - Running DNS Manager API Server in `http://localhost:5000/api/v1/`

### Setup Docker Deployment
* Make sure you are running on Linux Operating System (*this is because we need Celery and Gunicorn to start the API Server)
* Before running the Server, make sure you just create an environment variable in `.env` file
* There is 2 ways to deploy with Docker or Docker Compose
  * <b>Docker</b>
    * Go over in root directory
    * `docker build -t <your-username>/dnsmanager:tag . ` - Create DNS Manager API Server Image
    * `docker run -d -p 8080:8080 --name dnsmanager <your-username>/dnsmanager:tag` - Running DNS Manager API Server Container
    * This way you need to install redis in other container or just running in localhost
  * <b>Docker Compose</b>
    * Go over in root directory
    * If necessary make change on docker-compose.yml file for service configuration
    * `docker-compose up -d` - Up all service described at docker-compose.yml
    * With this way, you will need several container like:
      * `redis`
      * `postgresdb`
      * `dnsmanager`

### Additional Information
This DNS Manager API Server will work to communicate to your DNS Server on specific zone using <b>`Keyring`</b>, with this way its a best practice to communicate on DNS without directly changing on the db file.
If you have an existing DNS Zone that currently have record, with this DNS Manager Server API, we will import all the existing record from the registered zone. We also using a periodic task to check if there is a new record that not added from API and than added to the database.