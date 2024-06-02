```
curl -X POST http://localhost:8001/auto_annotate \
     -H "Content-Type: application/json" \
     -d '{"repo_path":"clvw42l9y0004t9pflhaqw3p7-test-auton-annotation","fiftyone_controller_endpoint":"http://192.168.9.14/skypilot/fiftyone-server-82de34-464f/8000","branch":"main","s3_endpoint_url":"http://datalake.qpiaipro.local","s3_access_key":"$ACCESS_KEY_ID","class_dict":{"person":"person","tank":"tank"},"s3_secret_key":"$SCECRET_ACCESS_KEY"}'
```