# Django Todo Application

A simple Todo application built with Django and PostgreSQL, containerized using Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1. Navigate to the project folder:

   ```bash
   cd TODO_APP
   ```

2. Build and run the containers using Docker Compose:

   ```bash
   docker compose up -d
   ```

3. Run the database migrations (if it's your first time or if you've added new models):

   ```bash
   docker compose exec web python manage.py migrate
   ```

4. Access the application in your browser at:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Project Structure

- `TODO_APP/` - The main Django project configuration (Settings, URLs, etc.)
- `todo/` - The Todo application logic
- `docker-compose.yml` - Defines the `web` (Django) and `db` (PostgreSQL) services
- `Dockerfile` - Builds the Django application image
- `requirements.txt` - Python dependencies needed for the project

## Useful Commands

- **Create an admin superuser:**

  ```bash
  docker compose exec web python manage.py createsuperuser
  ```

  _(You can then access the admin panel at `http://127.0.0.1:8000/admin`)_

- **Stop the containers:**

  ```bash
  docker compose down
  ```

- **View live logs:**

  ```bash
  docker compose logs -f web
  ```

- **Restart the application:**
  ```bash
  docker compose restart web
  ```

## Troubleshooting

### "Error loading MySQLdb module" when running Docker Compose

If you see an error like `django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module` in the container logs (`docker compose logs web`), this happens because `settings.py` was trying to load the MySQL backend while the Docker environment was set up to use PostgreSQL.

**How it was fixed:**
The database engine check in `TODO_APP/settings.py` was updated to correctly use `'django.db.backends.postgresql'` instead of `'django.db.backends.mysql'` whenever the `DB_HOST` environment variable is detected.

## First Create Node

**What it does:** Creates a Kubernetes cluster using Kind (Kubernetes in Docker).

**Use case:** Setting up a local development environment for testing Kubernetes applications.

**Destination:** Creates a local Kubernetes cluster on your machine.

**Simple explanation:** Think of this as building a playground where your apps will live. Just like you need a playground before you can play, you need a cluster before you can run apps.

### Steps:

1. **Install [Kind](https://github.com/Aditya-das-4707-e/install-kind-kubectl.sh)**
2. **Run this command:**
   ```bash
   kind create cluster --name <choose-a-name> --config=config.yml
   ```
   _Example:_
   ```bash
   kind create cluster --name my-first-cluster --config=config.yml
   ```

### To see your cluster

```bash
kind get clusters
```

### To see your nodes

```bash
kubectl get nodes
```

**Example Output:**

```text
NAME                               STATUS   ROLES           AGE   VERSION
adi-cloud-cluster-control-plane    Ready    control-plane   10m   v1.xx
adi-cloud-cluster-worker           Ready    <none>          10m   v1.xx
adi-cloud-cluster-worker2          Ready    <none>          10m   v1.xx
adi-cloud-cluster-worker3          Ready    <none>          10m   v1.xx
```

### Warning

To delete your cluster:

```bash
kind delete cluster --name <cluster_name>
```

## Kubernetes Troubleshooting & Issues Faced

<details>
<summary><b>1. Pods stuck in CrashLoopBackOff with MySQLdb Error</b></summary>

<br>

**Error message:** `django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module. Did you install mysqlclient?`

**What was the problem?**
The Kubernetes deployment was automatically pulling an older version of the image (`aditya81888/todo-app:latest`) directly from Docker Hub. That older image still expected a MySQL database instead of using the local updated code that was configured for PostgreSQL.

**How it was solved:**
1. Rebuilt the local Docker image with the latest `settings.py` changes:
   ```bash
   docker build -t aditya81888/todo-app:latest .
   ```
2. Loaded the newly built image into the local `kind` cluster:
   ```bash
   kind load docker-image aditya81888/todo-app:latest --name aditya-cluster
   ```
3. Updated the `deployment.yml` to prevent Kubernetes from pulling the outdated image from Docker Hub by adding `imagePullPolicy: IfNotPresent` to the web container spec.

</details>

<details>
<summary><b>2. Database relation "todo_task" does not exist</b></summary>

<br>

**Error message:** `relation "todo_task" does not exist` when visiting the application in the browser.

**What was the problem?**
The newly deployed PostgreSQL database in Kubernetes was completely empty. The required database tables (schema) for the Django application had not been created yet, so the app crashed when trying to fetch the todo tasks.

**How it was solved:**
Ran the Django migrations directly inside the running web container in Kubernetes to create the required database tables. This was done using the following command:
```bash
kubectl exec deployment/web-deployment -n todo -- python manage.py migrate
```

</details>
