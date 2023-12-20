# mantik - plugin for MLflow with HPC (UNICORE)

Mantik allows to manage the full Machine Learning workflow on HPC by
supporting MLflow and deployment of applications to HPC.

For a quickstart see [our documentation](https://mantik-ai.gitlab.io/mantik/client-quickstart.html)

## Extra Dependencies

By default, mantik only installs the core dependencies required to use the Mantik API.
However, additional extras are provided and can be installed:

- `mlflow`: installs the supported MLflow version (i.e. `mlflow-skinny` due do its much smaller size compared to `mlflow`)

  ```shell
  pip install "mantik[mlflow]"
  ```

- `s3`: installs the required dependencies to use the [S3 Remote File Service](https://mantik-ai.gitlab.io/mantik/remote-execution/remote-file-service.html)

  ```shell
  pip install "mantik[s3]"
  ```

- `unicore`: installs the required dependencies to use the [UNICORE Remote File Service](https://mantik-ai.gitlab.io/mantik/remote-execution/remote-file-service.html)

  ```shell
  pip install "mantik[unicore]"
  ```

## Helpdesk

For bug reports or feature requests, please email our helpdesk.
Details can be found [here](https://mantik-ai.gitlab.io/mantik/helpdesk.html).
