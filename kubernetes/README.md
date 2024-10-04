# QPIAI Pro Flyte Client Kubernetes Deployment

This folder contains the necessary Kubernetes configuration files to deploy the QPIAI Pro Flyte Client on a Kubernetes cluster.

## Prerequisites

- A Kubernetes cluster
- `kubectl` installed and configured to communicate with your cluster
- Docker image of your application pushed to a container registry accessible by your Kubernetes cluster

## Files

- `deployment.yaml`: Kubernetes Deployment configuration
- `service.yaml`: Kubernetes Service configuration for internal cluster access
- `azure-config.yaml`: ConfigMap for Azure-specific configuration
- `azure-secret.yaml`: Secret for Azure storage account credentials

## Setup and Deployment

1. Update the image in `deployment.yaml`:
   Replace `your-docker-registry/qpiai-pro-flyte-client:latest` with the actual image name and tag for your application.

2. (Optional) Update the `PORT` environment variable in `deployment.yaml` if your application uses a different port:
   ```yaml
   - name: PORT
     value: "8001"  # Change this if your app uses a different port
   ```

3. If you changed the port, also update the `targetPort` in `service.yaml`:
   ```yaml
   targetPort: 8001  # Change this to match the PORT in deployment.yaml
   ```

4. Ensure the `flyte` namespace exists in your cluster:
  ```
  kubectl create namespace flyte
  ```

5. Create the Secret:
   ```
   kubectl apply -f azure-secret.yaml -n flyte
   ```

6. Create the ConfigMap:
   ```
   kubectl apply -f azure-flyte-client-config.yaml -n flyte
   ```

7. Deploy the application:
   ```
   kubectl apply -f deployment.yaml -n flyte 
   ```

8. Create the Service:
   ```
   kubectl apply -f service.yaml -n flyte
   ```

9. Verify the deployment and service:
   ```
   kubectl get pods -n flyte
   kubectl get services -n flyte
   ```

   You should see a pod named `qpiai-pro-flyte-client-xxxxxx-xxxx` in the Running state and a service named `qpiai-pro-flyte-client-service`.

## Configuration

### Azure Configuration
The Azure configuration is stored in a ConfigMap and mounted into the container at `/app/config-azure.yaml`. Sensitive information (storage account name and key) is stored in a Kubernetes Secret and injected as environment variables.

To update the configuration:

1. For non-sensitive updates, modify the `azure-config.yaml` file and reapply:
   ```
   kubectl apply -f azure-config.yaml
   ```

2. For sensitive information, update the `azure-secret.yaml` file and reapply:
   ```
   kubectl apply -f azure-secret.yaml
   ```

### Application Port
The application port is set to 8001 by default. If you need to change this:

1. Update the `PORT` environment variable in `deployment.yaml`
2. Update the `targetPort` in `service.yaml`
3. Reapply both files:
   ```
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

After any configuration changes, restart the deployment to pick up the new configuration:
```
kubectl rollout restart deployment qpiai-pro-flyte-client
```

## Accessing the Service

The Flyte client is accessible within the cluster at `qpiai-pro-flyte-client-service:80`. This service forwards traffic to port 8001 (or your specified port) of your application. Other pods in the cluster can use this address to communicate with your Flyte client.

## Security Note

Sensitive information (Azure storage account name and key) is stored in a Kubernetes Secret. While this is more secure than storing it in a ConfigMap, for production environments, consider using a more robust secret management solution like Azure Key Vault with the CSI driver.

## Troubleshooting

If you encounter issues:

1. Check the pod status:
   ```
   kubectl get pods
   ```

2. If the pod is not in the Running state, check the logs:
   ```
   kubectl logs <pod-name>
   ```

3. For more detailed troubleshooting, you can describe the pod:
   ```
   kubectl describe pod <pod-name>
   ```

4. To check the service:
   ```
   kubectl describe service qpiai-pro-flyte-client-service
   ```

5. To check if the application is accessible within the cluster, you can use a temporary debug pod:
   ```
   kubectl run -it --rm debug --image=curlimages/curl -- sh
   # Once inside the debug pod:
   curl http://qpiai-pro-flyte-client-service:80
   ```

Replace `<pod-name>` with the actual name of your pod.

## Scaling

To scale the number of replicas:

```
kubectl scale deployment qpiai-pro-flyte-client --replicas=3
```

Replace `3` with the desired number of replicas.

## Updating the Application

To update the application to a new version:

1. Update the image tag in `deployment.yaml`
2. Apply the changes:
   ```
   kubectl apply -f deployment.yaml
   ```

Or, if you want to update the image without changing the yaml file:

```
kubectl set image deployment/qpiai-pro-flyte-client qpiai-pro-flyte-client=your-docker-registry/qpiai-pro-flyte-client:new-tag
```

Replace `new-tag` with the actual new version tag.

## Support

For additional support or questions, please contact the QPIAI Pro support team.