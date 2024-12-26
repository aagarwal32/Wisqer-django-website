1. Test Django
```
python manage.py test
```

2. Build Container
```
docker build -f Dockerfile --platform linux/amd64 \
    -t registry.digitalocean.com/django-wisqer-pcr/djangodocker:latest \
    -t registry.digitalocean.com/django-wisqer-pcr/djangodocker:v1 \
    .
```

3. Push container to DO Container Registry
```
docker push registry.digitalocean.com/django-wisqer-pcr/djangodocker --all-tags
```

4. Update secrets
```
kubectl delete secret django-wisqer-web-prod-env
kubectl create secret generic django-wisqer-web-prod-env --from-env-file=djangodocker/.env.prod
```

5. Update Deployment
```
kubectl apply -f wisqer-deployment/apps/django-wisqer-web.yaml
```

6. Wait for Rollout to Finish
```
kubectl rollout status deployment/django-wisqer-web-deployment
```

7. Migrate Database
```
export SINGLE_POD_NAME=$(kubectl get pod -l app=django-wisqer-web-deployment -o jsonpath="{.items[0].metadata.name}")
```
or
```
export SINGLE_POD_NAME=$(kubectl get pod -l=app=django-wisqer-web-deployment -o NAME | tail -n 1)
```

Run Migrations
```
kubectl exec -it $SINGLE_POD_NAME -- bash /app/migrate.sh
```